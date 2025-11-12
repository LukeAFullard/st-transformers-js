import streamlit as st
from st_transformers_js import transformers_js_pipeline_v2

st.title("st-transformers-js v2 Demo")

text_input = st.text_input("Enter text to send to the frontend:", "Hello from Python!")

response = transformers_js_pipeline_v2(text=text_input, key="v2_demo")

if response and "message" in response:
    st.write("Message from frontend:", response["message"])
