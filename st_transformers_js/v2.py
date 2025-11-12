import os
import base64
from typing import Union, Optional, Callable
import streamlit.components.v2 as components

COMPONENT_NAME = "st_transformers_js_v2"

# Verify build exists
ASSET_DIR = os.path.join(os.path.dirname(__file__), "frontend_v2", "dist")
if not os.path.exists(ASSET_DIR):
    raise RuntimeError(
        f"V2 component assets not found at {ASSET_DIR}. "
        "Run './build_script.sh' to build the frontend."
    )

_component_func = components.component(
    COMPONENT_NAME,
    html="index.html",
)

def transformers_js_pipeline_v2(
    model_name: str,
    pipeline_type: str,
    inputs: Union[str, bytes, dict],
    config: Optional[dict] = None,
    key: Optional[str] = None,
    on_change: Optional[Callable] = None,
) -> Optional[dict]:
    """
    Run a transformers.js pipeline in the browser (v2 component).

    Parameters
    ----------
    model_name : str
        Hugging Face model identifier
    pipeline_type : str
        Type of pipeline (e.g., "text-classification", "image-to-text")
    inputs : str, bytes, or dict
        Input data for the pipeline
    config : dict, optional
        Additional pipeline configuration
    key : str, optional
        Unique key for the component instance
    on_change : callable, optional
        Callback function when inference completes

    Returns
    -------
    BidiComponentResult
        Component result with status, progress, result, and error attributes
    """
    # Process inputs (keep existing logic)
    processed_inputs = inputs
    mime_type = None

    if isinstance(inputs, bytes):
        try:
            import magic
            mime_type = magic.from_buffer(inputs, mime=True)
        except Exception:
            if inputs.startswith(b'\x89PNG'):
                mime_type = 'image/png'
            elif inputs.startswith(b'\xff\xd8'):
                mime_type = 'image/jpeg'
            elif inputs.startswith(b'GIF'):
                mime_type = 'image/gif'
        processed_inputs = base64.b64encode(inputs).decode('utf-8')

    component_data = {
        "model_name": model_name,
        "pipeline_type": pipeline_type,
        "inputs": processed_inputs,
        "mime_type": mime_type,
        "config": config or {},
    }

    # Declare all state callbacks
    callback = on_change or (lambda: None)

    return _component_func(
        data=component_data,
        key=key,
        on_status_change=callback,
        on_progress_change=callback,
        on_result_change=callback,
        on_error_change=callback,
    )

__all__ = ["transformers_js_pipeline_v2"]
