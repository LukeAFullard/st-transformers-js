import base64
from typing import Union, Optional
import streamlit.components.v2 as components

COMPONENT_NAME = "st_transformers_js_v2"

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
) -> Optional[dict]:
    """
    Run a transformers.js pipeline in the browser (v2 component).
    """
    # Input validation
    if not isinstance(inputs, (str, bytes, dict)):
        raise TypeError(f"Input type not supported: {type(inputs)}. Must be str, bytes, or dict.")

    # Convert bytes to base64 if needed for image processing
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

    # Bundle arguments into a data dictionary
    component_data = {
        "model_name": model_name,
        "pipeline_type": pipeline_type,
        "inputs": processed_inputs,
        "mime_type": mime_type,
        "config": config if config is not None else {},
    }

    # Call the component
    return _component_func(data=component_data, key=key)

__all__ = ["transformers_js_pipeline_v2"]
