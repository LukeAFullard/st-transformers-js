import os
import streamlit.components.v1 as components
from typing import Optional

# Set _RELEASE to False when the STREAMLIT_COMPONENT_DEV_MODE env var is set
_RELEASE = not os.getenv("STREAMLIT_COMPONENT_DEV_MODE")
COMPONENT_NAME = "st_transformers_js_v2"

if not _RELEASE:
    # For local development, you can serve the frontend from a dev server
    _component_func = components.declare_component(
        COMPONENT_NAME,
        url="http://localhost:5174",
    )
else:
    # For release, Streamlit will serve the assets from the package's asset_dir
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend_v2/dist")
    _component_func = components.declare_component(
        COMPONENT_NAME,
        path=build_dir,
    )

def transformers_js_pipeline_v2(text: str, key: Optional[str] = None):
    """A simple v2 component."""
    return _component_func(text=text, key=key, default=None)

__all__ = ["transformers_js_pipeline_v2"]
