import streamlit as st
from st_transformers_js import transformers_js_pipeline_v2

st.title("st-transformers-js v2 Demo")
response = transformers_js_pipeline_v2(text="Hello v2!")
st.write("Response:", response)
