import streamlit as st
import os
import base64

# Set this to False for local development
_RELEASE = True

# The component name must be consistent with the one in pyproject.toml
COMPONENT_NAME = "transformers_js"

if not _RELEASE:
    # For local development, you can serve the frontend from a dev server
    _component_func = st.components.v2.component(
        COMPONENT_NAME,
        url="http://localhost:3001",
    )
else:
    # For release, Streamlit will serve the assets from the package's asset_dir
    _component_func = st.components.v2.component(COMPONENT_NAME)


def transformers_js_pipeline(
    model_name,
    pipeline_type,
    inputs,
    config=None,
    width=600,
    height=400,
    key=None
):
    """
    Run a transformers.js pipeline in the browser.
    
    Parameters:
    -----------
    model_name : str
        Hugging Face model identifier (e.g., "Xenova/donut-base-finetuned-cord-v2")
    pipeline_type : str
        Type of pipeline (e.g., "image-to-text", "text-classification", "token-classification")
    inputs : str, bytes, or dict
        Input data for the pipeline:
        - For image tasks: bytes or base64 string
        - For text tasks: string or dict with text
        - For other tasks: appropriate input format
    config : dict, optional
        Additional configuration for the pipeline
    width : int, optional
        Component width in pixels (default: 600)
    height : int, optional
        Component height in pixels (default: 400)
    key : str, optional
        Unique key for the component
    
    Returns:
    --------
    dict or None
        Pipeline output as JSON, or None if still processing
    """
    # Convert bytes to base64 if needed
    processed_inputs = inputs
    if isinstance(inputs, bytes):
        processed_inputs = base64.b64encode(inputs).decode('utf-8')
    
    # Prepare configuration for the frontend
    component_config = {
        "model_name": model_name,
        "pipeline_type": pipeline_type,
        "inputs": processed_inputs,
        "config": config or {}
    }
    
    # Call the component
    component_value = _component_func(
        config=component_config,
        width=width,
        height=height,
        key=key,
        default=None
    )
    
    return component_value


__version__ = "0.1.0"
__all__ = ["transformers_js_pipeline"]
