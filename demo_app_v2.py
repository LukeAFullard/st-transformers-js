import streamlit as st
from st_transformers_js import transformers_js_pipeline_v2
from PIL import Image, ImageDraw

st.set_page_config(layout="wide")

st.title("Transformers.js Streamlit Component (V2)")
st.info("This demo shows the V2 component, which uses modern Streamlit component architecture.")

# --- Helper function to display component status ---
def display_status(result):
    if not result:
        return False # Not running

    status = result.get("status")
    if status == "loading":
        st.info(f"Loading model '{result.get('message')}'...")
    elif status in ["download", "init"]:
        st.info(f"Downloading model... ({result.get('message')})")
        if result.get("progress"):
            st.progress(result.get("progress", 0) / 100)
    elif status == "processing":
        st.info("Running inference...")
    elif status == "complete":
        return False # Signal to stop running
    elif status == "error":
        st.error(f"An error occurred: {result.get('error')}")
        return False # Signal to stop running

    return True # Still running

# --- Text Classification Example ---
with st.container():
    st.header("1. Text Classification")
    text_input = st.text_area("Enter text to classify:", "I love Streamlit components!", key="text_input_v2")
    classify_btn = st.button("Classify Text", key="classify_btn_v2")

    if "text_clf_running" not in st.session_state:
        st.session_state.text_clf_running = False

    if classify_btn and text_input:
        st.session_state.text_clf_inputs = text_input
        st.session_state.text_clf_running = True
        st.session_state.pop("text_clf_result", None)

    if st.session_state.text_clf_running:
        result = transformers_js_pipeline_v2(
            model_name="Xenova/distilbert-base-uncased-finetuned-sst-2-english",
            pipeline_type="text-classification",
            inputs=st.session_state.text_clf_inputs,
            key="text_clf_v2",
        )
        st.session_state.text_clf_result = result
        if not display_status(result):
            st.session_state.text_clf_running = False
        st.rerun()

    if "text_clf_result" in st.session_state and st.session_state.text_clf_result:
        res = st.session_state.text_clf_result
        if res and res.get("status") == "complete":
            st.success("Classification complete!")
            st.json(res.get("result"))

# --- Image-to-Text Example ---
with st.container():
    st.header("2. Image-to-Text (OCR)")
    uploaded_file_ocr = st.file_uploader("Upload a document image", type=["jpg", "png", "jpeg"], key="ocr_uploader_v2")

    if "ocr_running" not in st.session_state:
        st.session_state.ocr_running = False

    if uploaded_file_ocr:
        st.image(uploaded_file_ocr, caption="Uploaded Document")
        if st.button("Extract Text", key="ocr_btn_v2"):
            st.session_state.ocr_inputs = uploaded_file_ocr.read()
            st.session_state.ocr_running = True
            st.session_state.pop("ocr_result", None)

    if st.session_state.ocr_running:
        result = transformers_js_pipeline_v2(
            model_name="Xenova/donut-base-finetuned-cord-v2",
            pipeline_type="image-to-text",
            inputs=st.session_state.ocr_inputs,
            key="ocr_v2",
        )
        st.session_state.ocr_result = result
        if not display_status(result):
            st.session_state.ocr_running = False
        st.rerun()

    if "ocr_result" in st.session_state and st.session_state.ocr_result:
        res = st.session_state.ocr_result
        if res and res.get("status") == "complete":
            st.success("Text extraction complete!")
            st.json(res.get("result"))

# --- Object Detection Example ---
with st.container():
    st.header("3. Object Detection")
    uploaded_file_obj = st.file_uploader("Upload an image for object detection", type=["jpg", "png", "jpeg"], key="obj_uploader_v2")

    if "obj_detect_running" not in st.session_state:
        st.session_state.obj_detect_running = False

    if uploaded_file_obj:
        image = Image.open(uploaded_file_obj)
        st.image(image, caption="Uploaded Image for Detection")

        if st.button("Detect Objects", key="obj_btn_v2"):
            st.session_state.obj_detect_inputs = uploaded_file_obj.getvalue()
            st.session_state.obj_detect_running = True
            st.session_state.pop("obj_detect_result", None)
            # Store image bytes to redraw boxes later
            st.session_state.obj_image_bytes = uploaded_file_obj.getvalue()


    if st.session_state.obj_detect_running:
        result = transformers_js_pipeline_v2(
            model_name="Xenova/detr-resnet-50",
            pipeline_type="object-detection",
            inputs=st.session_state.obj_detect_inputs,
            key="obj_detect_v2",
        )
        st.session_state.obj_detect_result = result
        if not display_status(result):
            st.session_state.obj_detect_running = False
        st.rerun()

    if "obj_detect_result" in st.session_state and st.session_state.obj_detect_result:
        res = st.session_state.obj_detect_result
        if res and res.get("status") == "complete":
            st.success("Object detection complete!")

            # Draw bounding boxes
            if "obj_image_bytes" in st.session_state:
                from io import BytesIO
                image = Image.open(BytesIO(st.session_state.obj_image_bytes))
                draw = ImageDraw.Draw(image)
                for detection in res.get("result", []):
                    box = detection.get("box", {})
                    label = detection.get("label", "N/A")
                    score = round(detection.get("score", 0), 2)
                    xmin, ymin, xmax, ymax = box.get("xmin", 0), box.get("ymin", 0), box.get("xmax", 0), box.get("ymax", 0)
                    draw.rectangle((xmin, ymin, xmax, ymax), outline="red", width=3)
                    draw.text((xmin, ymin), f"{label} ({score})", fill="red")
                st.image(image, caption="Image with Bounding Boxes")

            st.json(res.get("result"))
