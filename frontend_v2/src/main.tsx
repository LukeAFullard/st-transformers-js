import { Component, ComponentState } from "@streamlit/component-v2-lib"
import React, { useState, useEffect } from "react"
import { createRoot } from "react-dom/client"
import { pipeline, env } from "@xenova/transformers";

// Skip local model checks for faster loading in a web environment.
env.allowLocalModels = false;

interface ComponentData {
    model_name: string;
    pipeline_type: any;
    inputs: string | undefined;
    mime_type: string | undefined;
    config: object | undefined;
}

interface ComponentStatus extends ComponentState {
    status: string;
    message: string;
    progress?: number;
    result?: any;
    error?: string;
}

const TransformersComponent: React.FC<{ data: ComponentData; setStateValue: (name: string, value: any) => void }> = ({ data, setStateValue }) => {
    const [message, setMessage] = useState("Component loaded.");
    const [progress, setProgress] = useState<number | undefined>(undefined);

     // --- Unified State Update Function ---
     const updateState = (newState: Partial<ComponentStatus>) => {
        // Update UI
        if (newState.message) {
            setMessage(newState.message);
        }
       setProgress(newState.progress);


        // Send state back to Python for each key
        for (const [key, value] of Object.entries(newState)) {
            setStateValue(key.toString(), value);
        }
    };


    useEffect(() => {
        const runPipeline = async (retries = 3) => {
            for (let attempt = 1; attempt <= retries; attempt++) {
                try {
                    updateState({
                        status: "loading",
                        message: `Loading model: ${data.model_name} (attempt ${attempt}/${retries})`,
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

                    // Success, exit the loop
                    return;

                } catch (error: any) {
                    console.error(`Pipeline error (attempt ${attempt}/${retries}):`, error);
                    if (attempt === retries) {
                        updateState({
                            status: "error",
                            message: `Error: ${error.message}`,
                            error: error.message,
                            progress: undefined, // Hide progress bar
                        });
                    } else {
                        updateState({
                            status: "error",
                            message: `Download failed. Retrying in ${attempt * 2}s...`,
                            progress: undefined,
                        });
                        await new Promise(resolve => setTimeout(resolve, attempt * 2000));
                    }
                }
            }
        };
        runPipeline();
    }, [data.model_name, data.pipeline_type, data.inputs, data.config, data.mime_type]);


    return (
        <div>
            <p>{message}</p>
            {progress !== undefined && <progress value={progress} max="100" style={{ width: "100%" }} />}
        </div>
    )
}

const StTransformersComponent: Component = (args) => {
    const rootEl = args.parentElement.querySelector('#root');
    if (rootEl) {
        const root = createRoot(rootEl);
        root.render(
            <React.StrictMode>
                <TransformersComponent data={args.data as unknown as ComponentData} setStateValue={args.setStateValue} />
            </React.StrictMode>
        );
    } else {
        console.error("Root element not found");
    }
};

export default StTransformersComponent;
