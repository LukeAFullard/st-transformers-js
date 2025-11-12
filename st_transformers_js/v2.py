import streamlit.components.v2 as components
from typing import Optional

COMPONENT_NAME = "st_transformers_js_v2"

# With the v2 component API, the component is declared once.
# Streamlit handles serving the component from the specified asset_dir in pyproject.toml
# during production, and from the dev server during development (if STREAMLIT_COMPONENT_DEV_MODE=1).
_component_func = components.component(
    COMPONENT_NAME,
    html="index.html",
)

def transformers_js_pipeline_v2(text: str, key: Optional[str] = None):
    """A simple v2 component."""
    return _component_func(data={"text": text}, key=key)

__all__ = ["transformers_js_pipeline_v2"]
