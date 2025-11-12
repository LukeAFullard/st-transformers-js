"""
Demo application for st-transformers-js v2 component
Tests multiple pipeline types with different models
"""
import streamlit as st
from st_transformers_js import transformers_js_pipeline_v2

st.set_page_config(
    page_title="Transformers.js v2 Demo",
    page_icon="🤗",
    layout="wide"
)

st.title("🤗 Transformers.js in Streamlit (v2 Component)")
st.markdown("Run Hugging Face models entirely in your browser - no backend required!")

# Sidebar for selecting demo
demo_type = st.sidebar.selectbox(
    "Select Demo",
    ["Text Classification", "Image to Text (Donut)", "Token Classification (NER)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This component runs transformers.js models entirely in the browser using WebAssembly. "
    "Models are downloaded once and cached locally."
)

# Shared session state to store results
if "result_v2" not in st.session_state:
    st.session_state.result_v2 = None

# ===== TEXT CLASSIFICATION =====
if demo_type == "Text Classification":
    st.header("📝 Text Classification")
    st.markdown("Analyze sentiment using DistilBERT")

    text_input = st.text_area(
        "Enter text to classify:",
        value="I absolutely love using Streamlit! It makes building ML apps so easy.",
        height=100
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        classify_btn = st.button("Classify", type="primary", use_container_width=True)

    if classify_btn and text_input:
        st.session_state.result_v2 = transformers_js_pipeline_v2(
            model_name="Xenova/distilbert-base-uncased-finetuned-sst-2-english",
            pipeline_type="text-classification",
            inputs=text_input,
            key="text_clf_v2"
        )

# ===== IMAGE TO TEXT (DONUT) =====
elif demo_type == "Image to Text (Donut)":
    st.header("🖼️ Document OCR with Donut")
    st.markdown("Extract structured data from receipts and documents")

    uploaded_file = st.file_uploader(
        "Upload a receipt or document image",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of a receipt or invoice"
    )

    if uploaded_file is not None:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        with col2:
            if st.button("Extract Text", type="primary"):
                img_bytes = uploaded_file.read()
                st.session_state.result_v2 = transformers_js_pipeline_v2(
                    model_name="Xenova/donut-base-finetuned-cord-v2",
                    pipeline_type="image-to-text",
                    inputs=img_bytes,
                    key="ocr_v2"
                )
    else:
        st.info("👆 Upload an image to get started")

# ===== TOKEN CLASSIFICATION (NER) =====
elif demo_type == "Token Classification (NER)":
    st.header("🏷️ Named Entity Recognition")
    st.markdown("Extract people, organizations, and locations from text")

    text_input = st.text_area(
        "Enter text for entity extraction:",
        value="Apple Inc. was founded by Steve Jobs in Cupertino, California. "
              "The company is now led by Tim Cook and has offices in London and Tokyo.",
        height=100
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        extract_btn = st.button("Extract Entities", type="primary", use_container_width=True)

    if extract_btn and text_input:
        st.session_state.result_v2 = transformers_js_pipeline_v2(
            model_name="Xenova/bert-base-NER",
            pipeline_type="token-classification",
            inputs=text_input,
            config={"aggregation_strategy": "simple"},
            key="ner_v2"
        )

# --- Display component status and results ---
if st.session_state.result_v2:
    status = st.session_state.result_v2.get("status", "idle")
    message = st.session_state.result_v2.get("message", "")
    progress = st.session_state.result_v2.get("progress")
    result = st.session_state.result_v2.get("result")
    error = st.session_state.result_v2.get("error")

    if status in ["loading", "processing", "download"] and message:
        with st.spinner(message):
            if progress:
                st.progress(progress / 100)
            st.empty() # Keep the spinner running

    if error:
        st.error(f"An error occurred: {error}")

    if result:
        st.success("Processing Complete!")
        st.json(result)

# Footer
st.markdown("---")
st.markdown(
    "Built with [Streamlit](https://streamlit.io) and "
    "[Transformers.js](https://github.com/xenova/transformers.js)"
)
