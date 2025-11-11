import streamlit as st
from st_transformers_js import transformers_js_pipeline
from PIL import Image
import io

st.set_page_config(layout="wide")

st.title("Transformers.js Streamlit Component")
st.header("Image-to-Text Example")

# Example: Document Query Answering with Donut
st.subheader("Document Query Answering")
st.write(
    "This example uses the `Xenova/donut-base-finetuned-cord-v2` model to answer questions about a document image."
)

# Upload image
image_file = st.file_uploader(
    "Upload a document image (e.g., a receipt)",
    type=["png", "jpg", "jpeg"]
)

if image_file:
    # To read file as bytes:
    image_bytes = image_file.getvalue()
    # To convert to a PIL Image object:
    image = Image.open(io.BytesIO(image_bytes))

    st.image(image, caption="Uploaded Document", use_column_width=True)

    # Define query
    query = st.text_input(
        "Enter a question about the document:",
        value="What is the total amount?"
    )

    if st.button("Run Document Query"):
        with st.spinner("Running inference..."):
            # Run the pipeline
            result = transformers_js_pipeline(
                model_name="Xenova/donut-base-finetuned-cord-v2",
                pipeline_type="document-question-answering",
                inputs=image_bytes,
                config={"question": query},
                key="doc_query",
            )

        st.subheader("Result")
        st.json(result)
        print(f"Document Query Result: {result}")

# Example: Text Classification
st.header("Text Classification Example")
st.subheader("Sentiment Analysis")

text_input = st.text_area(
    "Enter text for sentiment analysis:",
    value="This is a fantastic component!"
)

if st.button("Run Sentiment Analysis"):
    with st.spinner("Running inference..."):
        result = transformers_js_pipeline(
            model_name="Xenova/distilbert-base-uncased-finetuned-sst-2-english",
            pipeline_type="text-classification",
            inputs=text_input,
            key="sentiment",
        )

    st.subheader("Result")
    st.json(result)
    print(f"Sentiment Analysis Result: {result}")
