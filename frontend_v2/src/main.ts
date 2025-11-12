import { Component, ComponentState } from "@streamlit/component-v2-lib";
import { pipeline, env } from "@xenova/transformers";

// Skip local model checks for faster loading in a web environment.
env.allowLocalModels = false;

/**
 * The data shape for the component's input from Python.
 */
interface ComponentData {
    model_name: string;
    pipeline_type: any; // Using `any` to match transformers.js flexibility
    inputs: string | undefined; // Can be text or base64 image
    mime_type: string | undefined;
    config: object | undefined;
}

/**
 * The component's state, which is sent back to Python.
 */
interface ComponentStatus extends ComponentState {
    status: string;
    message: string;
    progress?: number;
    result?: any;
    error?: string;
}

/**
 * Main component function.
 */
const MyComponent: Component<ComponentStatus, ComponentData> = (args) => {
    const { data, setStateValue, parentElement } = args;

    // --- UI Setup ---
    const root = document.createElement("div");
    root.style.fontFamily = "sans-serif";
    const statusEl = document.createElement("p");
    const progressEl = document.createElement("progress");
    progressEl.style.width = "100%";
    progressEl.style.display = "none";
    root.append(statusEl, progressEl);
    parentElement.appendChild(root);

    // --- State Update Function ---
    const updateStatus = (status: string, message: string, progress?: number) => {
        statusEl.textContent = message;
        if (progress !== undefined) {
            progressEl.value = progress;
            progressEl.style.display = "block";
        } else {
            progressEl.style.display = "none";
        }
        // Set state values individually, as expected by component-v2-lib v0.1.0
        setStateValue("status", status);
        setStateValue("message", message);
        setStateValue("progress", progress);
    };

    // --- Main Pipeline Logic ---
    const runPipeline = async () => {
        try {
            updateStatus("loading", `Loading model: ${data.model_name}`);
            const pipe = await pipeline(data.pipeline_type, data.model_name, {
                progress_callback: (progress: any) => {
                    updateStatus(
                        progress.status,
                        `[${progress.status}] ${progress.file} (${Math.round(progress.progress)}%)`,
                        progress.progress
                    );
                },
            });

            updateStatus("processing", "Running inference...");
            let processedInputs = data.inputs;
            if (data.mime_type && data.mime_type.startsWith("image/")) {
                // Handle image inputs (decode base64)
                processedInputs = `data:${data.mime_type};base64,${data.inputs}`;
            }

            const result = await pipe(processedInputs, data.config);

            updateStatus("complete", "Inference complete!");
            setStateValue("result", result);

        } catch (error: any) {
            console.error("Pipeline error:", error);
            updateStatus("error", `Error: ${error.message}`);
            setStateValue("error", error.message);
        }
    };

    // Run the pipeline when the component is mounted.
    runPipeline();
};

export default MyComponent;
