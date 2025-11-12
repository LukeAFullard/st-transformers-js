import streamlit as st
from st_transformers_js import transformers_js_pipeline_v2
from PIL import Image, ImageDraw

st.set_page_config(layout="wide")

st.title("Transformers.js Streamlit Component (V2)")
st.info("This demo shows the V2 component, which uses modern Streamlit component architecture.")

# --- Text Classification Example ---
with st.container():
    st.header("1. Text Classification")
    st.markdown(
        "This example performs sentiment analysis on the input text "
        "using the `Xenova/distilbert-base-uncased-finetuned-sst-2-english` model."
    )

    text_input = st.text_area(
        "Enter text to classify:",
        "I love Streamlit components!",
        key="text_input_v2"
    )
    classify_btn = st.button("Classify Text", key="classify_btn_v2")

    if classify_btn and text_input:
        # Clear previous results before running
        st.session_state.pop("text_clf_v2", None)

        # The component now returns a result object with attributes
        result = transformers_js_pipeline_v2(
            model_name="Xenova/distilbert-base-uncased-finetuned-sst-2-english",
            pipeline_type="text-classification",
            inputs=text_input,
            key="text_clf_v2",
            on_change=lambda: st.rerun(),  # Trigger a rerun on state changes
        )

        # Display status based on the result object's attributes
        if result:
            if result.status == "loading":
                st.info(f"Loading model '{result.message}'...")
            elif result.status in ["download", "init"]:
                st.info(f"Downloading model... ({result.message})")
                if result.progress:
                    st.progress(result.progress / 100)
            elif result.status == "processing":
                st.info("Running inference...")
            elif result.status == "complete" and result.result:
                st.success("Classification complete!")
                st.json(result.result)
            elif result.error:
                st.error(f"An error occurred: {result.error}")
            else:
                # Fallback for any other state
                st.write(f"Component state: {result}")


# --- Image-to-Text Example ---
with st.container():
    st.header("2. Image-to-Text (OCR)")
    st.markdown(
        "Upload a document image to extract text using the "
        "`Xenova/donut-base-finetuned-cord-v2` model."
    )

    uploaded_file_ocr = st.file_uploader(
        "Upload a document image",
        type=["jpg", "png", "jpeg"],
        key="ocr_uploader_v2"
    )

    if uploaded_file_ocr:
        st.image(uploaded_file_ocr, caption="Uploaded Document")
        if st.button("Extract Text", key="ocr_btn_v2"):
            # Clear previous results before running
            st.session_state.pop("ocr_v2", None)

            img_bytes = uploaded_file_ocr.read()

            result_ocr = transformers_js_pipeline_v2(
                model_name="Xenova/donut-base-finetuned-cord-v2",
                pipeline_type="image-to-text",
                inputs=img_bytes,
                key="ocr_v2",
                on_change=lambda: st.rerun(),
            )

            if result_ocr:
                if result_ocr.status in ["download", "init"]:
                    st.info(f"Downloading model... ({result_ocr.message})")
                    if result_ocr.progress:
                        st.progress(result_ocr.progress / 100)
                elif result_ocr.status == "complete" and result_ocr.result:
                    st.success("Text extraction complete!")
                    st.json(result_ocr.result)
                elif result_ocr.error:
                    st.error(f"Error: {result_ocr.error}")


# --- Object Detection Example ---
with st.container():
    st.header("3. Object Detection")
    st.markdown(
        "Upload an image to detect objects using the `Xenova/detr-resnet-50` model. "
        "Bounding boxes will be drawn on the image."
    )

    uploaded_file_obj = st.file_uploader(
        "Upload an image for object detection",
        type=["jpg", "png", "jpeg"],
        key="obj_uploader_v2"
    )

    if uploaded_file_obj:
        image = Image.open(uploaded_file_obj)
        st.image(image, caption="Uploaded Image for Detection")

        if st.button("Detect Objects", key="obj_btn_v2"):
            # Clear previous results before running
            st.session_state.pop("obj_detect_v2", None)

            img_bytes = uploaded_file_obj.getvalue()

            result_obj = transformers_js_pipeline_v2(
                model_name="Xenova/detr-resnet-50",
                pipeline_type="object-detection",
                inputs=img_bytes,
                key="obj_detect_v2",
                on_change=lambda: st.rerun(),
            )

            if result_obj:
                if result_obj.status in ["download", "init"]:
                    st.info(f"Downloading model... ({result_obj.message})")
                    if result_obj.progress:
                        st.progress(result_obj.progress / 100)
                elif result_obj.status == "complete" and result_obj.result:
                    st.success("Object detection complete!")

                    # Draw bounding boxes
                    draw = ImageDraw.Draw(image)
                    for detection in result_obj.result:
                        box = detection["box"]
                        label = detection["label"]
                        score = round(detection["score"], 2)

                        xmin, ymin, xmax, ymax = box.values()
                        draw.rectangle((xmin, ymin, xmax, ymax), outline="red", width=3)
                        draw.text((xmin, ymin), f"{label} ({score})", fill="red")

                    st.image(image, caption="Image with Bounding Boxes")
                    st.json(result_obj.result)
                elif result_obj.error:
                    st.error(f"Error: {result_obj.error}")
