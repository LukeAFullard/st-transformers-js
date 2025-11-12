import streamlit as st
import streamlit.components.v1 as components
import os
import base64
from typing import Union, Optional

# Set _RELEASE to False when the STREAMLIT_COMPONENT_DEV_MODE env var is set
_RELEASE = not os.getenv("STREAMLIT_COMPONENT_DEV_MODE")

# The component name must be consistent with the one in pyproject.toml
COMPONENT_NAME = "st_transformers_js"

if not _RELEASE:
    # For local development, you can serve the frontend from a dev server
    _component_func = components.declare_component(
        COMPONENT_NAME,
        url="http://localhost:5173",
    )
else:
    # For release, Streamlit will serve the assets from the package's asset_dir
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        COMPONENT_NAME,
        path=build_dir,
    )


def transformers_js_pipeline(
    model_name: str,
    pipeline_type: str,
    inputs: Union[str, bytes, dict],
    config: Optional[dict] = None,
    width: int = 600,
    height: int = 400,
    key: Optional[str] = None,
) -> Optional[dict]:
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
    key : str, optional
        Unique key for the component

    Returns:
    --------
    dict or None
        Pipeline output as JSON, or None if still processing
    """
    # Input validation
    if not isinstance(inputs, (str, bytes, dict)):
        raise TypeError(f"Input type not supported: {type(inputs)}. Must be str, bytes, or dict.")

    # Convert bytes to base64 if needed
    processed_inputs = inputs
    mime_type = None
    if isinstance(inputs, bytes):
        try:
            import magic
            mime_type = magic.from_buffer(inputs, mime=True)
        except Exception:
            # Fallback to manual detection
            if inputs.startswith(b'\x89PNG'):
                mime_type = 'image/png'
            elif inputs.startswith(b'\xff\xd8'):
                mime_type = 'image/jpeg'
            elif inputs.startswith(b'GIF'):
                mime_type = 'image/gif'
        processed_inputs = base64.b64encode(inputs).decode('utf-8')

    # Call the component
    component_value = _component_func(
        pipeline_type=pipeline_type,
        model_name=model_name,
        inputs=processed_inputs,
        mime_type=mime_type,
        config=config if config is not None else {},
        width=width,
        height=height,
        key=key,
        default=None
    )

    return component_value


__version__ = "0.1.0"
__all__ = ["transformers_js_pipeline"]
