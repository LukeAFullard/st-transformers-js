import streamlit as st
from st_transformers_js.v2 import st_transformers_js_v2

st.title("st-transformers-js v2 Demo")
response = st_transformers_js_v2(text="Hello v2!")
st.write("Response:", response)
