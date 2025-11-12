import os
import streamlit.components.v2 as components

_component_func = components.component(
    "st_transformers_js_v2",
    html='<div class="component-root"><h1></h1></div>',
    js="index.js"
)

def st_transformers_js_v2(text: str, key=None):
    return _component_func(text=text, key=key, default=None)
