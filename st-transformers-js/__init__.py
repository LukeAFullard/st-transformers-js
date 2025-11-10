import streamlit.components.v1 as components
import os
import base64

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "transformers_js",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("transformers_js", path=build_dir)


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
    
    Examples:
    ---------
    >>> # Image to text
    >>> with open("receipt.jpg", "rb") as f:
    ...     img_bytes = f.read()
    >>> result = transformers_js_pipeline(
    ...     "Xenova/donut-base-finetuned-cord-v2",
    ...     "image-to-text",
    ...     img_bytes
    ... )
    
    >>> # Text classification
    >>> result = transformers_js_pipeline(
    ...     "Xenova/distilbert-base-uncased-finetuned-sst-2-english",
    ...     "text-classification",
    ...     "I love this product!"
    ... )
    """
    # Convert bytes to base64 if needed
    processed_inputs = inputs
    if isinstance(inputs, bytes):
        processed_inputs = base64.b64encode(inputs).decode('utf-8')
    
    # Prepare configuration
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
