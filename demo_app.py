"""
Demo application for st-transformers-js component
Tests multiple pipeline types with different models
"""

import streamlit as st
from st_transformers_js import transformers_js_pipeline

st.set_page_config(
    page_title="Transformers.js Demo",
    page_icon="🤗",
    layout="wide"
)

st.title("🤗 Transformers.js in Streamlit")
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
        with st.spinner("Loading model and running inference..."):
            result = transformers_js_pipeline(
                model_name="Xenova/distilbert-base-uncased-finetuned-sst-2-english",
                pipeline_type="text-classification",
                inputs=text_input,
                height=300
            )
        
        if result and not result.get('error'):
            st.success("Classification complete!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Label", result[0]['label'])
            with col2:
                st.metric("Confidence", f"{result[0]['score']:.2%}")
            
            st.json(result)
        elif result and result.get('error'):
            st.error(f"Error: {result['error']}")

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
                
                with st.spinner("Loading Donut model and processing image..."):
                    result = transformers_js_pipeline(
                        model_name="Xenova/donut-base-finetuned-cord-v2",
                        pipeline_type="image-to-text",
                        inputs=img_bytes,
                        height=400
                    )
                
                if result and not result.get('error'):
                    st.success("Extraction complete!")
                    st.json(result)
                elif result and result.get('error'):
                    st.error(f"Error: {result['error']}")
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
        with st.spinner("Loading NER model and extracting entities..."):
            result = transformers_js_pipeline(
                model_name="Xenova/bert-base-NER",
                pipeline_type="token-classification",
                inputs=text_input,
                config={"aggregation_strategy": "simple"},
                height=300
            )
        
        if result and not result.get('error'):
            st.success("Extraction complete!")
            
            # Group entities by type
            entities_by_type = {}
            for entity in result:
                entity_type = entity['entity_group']
                if entity_type not in entities_by_type:
                    entities_by_type[entity_type] = []
                entities_by_type[entity_type].append(entity)
            
            # Display grouped entities
            cols = st.columns(len(entities_by_type))
            for idx, (entity_type, entities) in enumerate(entities_by_type.items()):
                with cols[idx]:
                    st.markdown(f"**{entity_type}**")
                    for entity in entities:
                        st.markdown(f"- {entity['word']} ({entity['score']:.2%})")
            
            st.markdown("---")
            st.markdown("**Full Results:**")
            st.json(result)
        elif result and result.get('error'):
            st.error(f"Error: {result['error']}")

# Footer
st.markdown("---")
st.markdown(
    "Built with [Streamlit](https://streamlit.io) and "
    "[Transformers.js](https://github.com/xenova/transformers.js)"
)
