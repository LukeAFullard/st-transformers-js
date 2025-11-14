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
const TransformersComponent: Component<ComponentStatus, ComponentData> = (args) => {
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

    // --- Unified State Update Function ---
    const updateState = (newState: Partial<ComponentStatus>) => {
        // Update UI
        if (newState.message) {
            statusEl.textContent = newState.message;
        }
        if (newState.progress !== undefined) {
            progressEl.value = newState.progress;
            progressEl.style.display = "block";
        } else if (newState.progress === undefined) {
            // Hide progress bar if progress is explicitly set to undefined
            progressEl.style.display = "none";
        }

        // Send state back to Python for each key
        for (const [key, value] of Object.entries(newState)) {
            setStateValue(key as keyof ComponentStatus, value);
        }
    };

    // --- Main Pipeline Logic ---
    const runPipeline = async () => {
        try {
            updateState({
                status: "loading",
                message: `Loading model: ${data.model_name}`
            });

            const pipe = await pipeline(data.pipeline_type, data.model_name, {
                progress_callback: (progress: any) => {
                    updateState({
                        status: progress.status,
                        message: `[${progress.status}] ${progress.file} (${Math.round(progress.progress)}%)`,
                        progress: progress.progress,
                    });
                },
            });

            updateState({
                status: "processing",
                message: "Running inference...",
                progress: undefined, // Hide progress bar
            });

            let processedInputs = data.inputs;
            if (data.mime_type && data.mime_type.startsWith("image/")) {
                processedInputs = `data:${data.mime_type};base64,${data.inputs}`;
            }

            const result = await pipe(processedInputs, data.config);

            updateState({
                status: "complete",
                message: "Inference complete!",
                result: result,
                progress: undefined, // Hide progress bar
            });

        } catch (error: any) {
            console.error("Pipeline error:", error);
            updateState({
                status: "error",
                message: `Error: ${error.message}`,
                error: error.message,
                progress: undefined, // Hide progress bar
            });
        }
    };

    // Run the pipeline when the component is mounted.
    runPipeline();
};

export default TransformersComponent;
