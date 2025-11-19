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

    Returns
    -------
    dict or None
        A dictionary with the component's state (status, progress, etc.)
    """
    from .helpers import process_inputs

    # Validate required parameters
    if not model_name or not pipeline_type:
        raise ValueError("model_name and pipeline_type are required")

    # Process inputs with error handling
    try:
        processed_inputs, mime_type = process_inputs(inputs)
    except TypeError as e:
        raise TypeError(
            f"Invalid input type for transformers pipeline. {str(e)}"
        ) from e
    except ValueError as e:
        raise ValueError(
            f"Failed to process pipeline inputs. {str(e)}"
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"Unexpected error processing inputs: {str(e)}"
        ) from e

    component_data = {
        "model_name": model_name,
        "pipeline_type": pipeline_type,
        "inputs": processed_inputs,
        "mime_type": mime_type,
        "config": config or {},
    }

    return _component_func(data=component_data, key=key)

__all__ = ["transformers_js_pipeline_v2"]
