# st-transformers-js

A fully **offline Streamlit component** for running Hugging Face Transformers.js models in the browser. Works seamlessly with Streamlit Cloud, stlite, and Pyodide environments.

## ✨ Features

- **V2 and V1 Components:** Ships with a modern, recommended V2 component and a legacy V1 component for backward compatibility.
- **Fully Offline:** Bundles `transformers.js` locally, no CDN dependencies.
- **Zero Backend:** Models run entirely in the browser via WebAssembly.
- **All Pipeline Types:** Supports object-detection, image-to-text, text-classification, and more.
- **Progress Logging (V2):** Real-time feedback on model downloads and processing.

## 📦 Installation

```bash
pip install st-transformers-js
# For image processing, you may need python-magic and Pillow
pip install python-magic Pillow
```

---

## 🚀 V2 Component Guides (Recommended)

The V2 component is the modern, preferred way to use this library. It offers real-time status updates from the frontend.

**Import the V2 component:**
```python
from st_transformers_js import transformers_js_pipeline_v2
```

### Example 1: Text Classification

This example classifies text sentiment using a DistilBERT model.

```python
import streamlit as st
from st_transformers_js import transformers_js_pipeline_v2

st.header("V2 Text Classification")

text_input = st.text_area("Enter text to classify:", "I love Streamlit components!")
if st.button("Classify Text"):
    if text_input:
        result = transformers_js_pipeline_v2(
            model_name="Xenova/distilbert-base-uncased-finetuned-sst-2-english",
            pipeline_type="text-classification",
            inputs=text_input,
            key="text_clf_v2"
        )
        st.session_state.result_v2 = result

# Display status and results from session state
if "result_v2" in st.session_state and st.session_state.result_v2:
    res = st.session_state.result_v2
    if res:
        if res.status == "loading":
            st.info(f"Loading model '{res.message}'...")
        elif res.status in ["download", "init"]:
            st.info(f"Downloading model... ({res.message})")
            if res.progress:
                st.progress(res.progress / 100)
        elif res.status == "processing":
            st.info("Running inference...")
        elif res.status == "complete" and res.result:
            st.success("Classification complete!")
            st.json(res.result)
        elif res.error:
            st.error(f"An error occurred: {res.error}")
```

### Example 2: Image-to-Text (OCR)

This example extracts text from an uploaded document image using a Donut model.

```python
import streamlit as st
from st_transformers_js import transformers_js_pipeline_v2

st.header("V2 Image-to-Text (OCR)")

uploaded_file = st.file_uploader("Upload a document image", type=["jpg", "png"])
if uploaded_file:
    st.image(uploaded_file)
    if st.button("Extract Text"):
        img_bytes = uploaded_file.read()
        result = transformers_js_pipeline_v2(
            model_name="Xenova/donut-base-finetuned-cord-v2",
            pipeline_type="image-to-text",
            inputs=img_bytes,
            key="ocr_v2"
        )
        st.session_state.result_ocr_v2 = result

# Display status and results
if "result_ocr_v2" in st.session_state and st.session_state.result_ocr_v2:
    res = st.session_state.result_ocr_v2
    if res:
        if res.status in ["download", "init"]:
            st.info(f"Downloading model... ({res.message})")
            if res.progress:
                st.progress(res.progress / 100)
        elif res.status == "complete" and res.result:
            st.success("Extraction complete!")
            st.json(res.result)
        elif res.error:
            st.error(f"An error occurred: {res.error}")
```

### Example 3: Object Detection

This example detects objects in an image and draws bounding boxes around them.

```python
import streamlit as st
from st_transformers_js import transformers_js_pipeline_v2
from PIL import Image, ImageDraw

st.header("V2 Object Detection")

uploaded_file = st.file_uploader("Upload an image for object detection", type=["jpg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    if st.button("Detect Objects"):
        img_bytes = uploaded_file.getvalue()
        result = transformers_js_pipeline_v2(
            model_name="Xenova/detr-resnet-50",
            pipeline_type="object-detection",
            inputs=img_bytes,
            key="obj_detect_v2"
        )
        st.session_state.result_obj_v2 = result

# Display results and draw bounding boxes
if "result_obj_v2" in st.session_state and st.session_state.result_obj_v2:
    res = st.session_state.result_obj_v2
    if res:
        if res.status in ["download", "init"]:
            st.info(f"Downloading model... ({res.message})")
            if res.progress:
                st.progress(res.progress / 100)
        elif res.status == "complete" and res.result:
            st.success("Object detection complete!")

            # Draw bounding boxes
            draw = ImageDraw.Draw(image)
            for detection in res.result:
                box = detection["box"]
                label = detection["label"]
                score = round(detection["score"], 2)

                xmin, ymin, xmax, ymax = box.values()
                draw.rectangle((xmin, ymin, xmax, ymax), outline="red", width=2)
                draw.text((xmin, ymin), f"{label} ({score})", fill="red")

            st.image(image, caption="Image with Bounding Boxes")
            st.json(res.result)
        elif res.error:
            st.error(f"An error occurred: {res.error}")
```

---

## 📖 API Reference

### V2 Component (Recommended)

`transformers_js_pipeline_v2(model_name, pipeline_type, inputs, config=None, key=None, on_change=None)`

- **`model_name`**: Hugging Face model identifier.
- **`pipeline_type`**: The task pipeline to use (e.g., "object-detection").
- **`inputs`**: Input data (text string or image bytes).
- **`config`**: Optional dictionary for pipeline configuration.
- **`key`**: A unique Streamlit key for the component instance.
- **`on_change`**: An optional callback function that will be called when the component's state changes.
- **Returns**: A `BidiComponentResult` object with the component's state.

### V1 Component (Legacy)

`transformers_js_pipeline_v1(model_name, pipeline_type, inputs, config=None, width=600, height=400, key=None)`

- **Parameters**: Same as V2, with the addition of `width` and `height` for the component's iframe.
- **Returns**: The final JSON result from the pipeline, or `None` while processing.

---

## 🛠️ Development Setup

### Project Structure

```
.
├── frontend_v2/
├── st_transformers_js/
│   ├── v1.py, v2.py
│   ├── frontend_v1/
│   └── frontend_v2/dist/
├── tests/
├── demo_app.py, demo_app_v2.py
└── build_script.sh
```

### Setup Instructions

1.  **Install Dependencies:** `pip install -e .`
2.  **Build Frontend Assets:** `./build_script.sh`
3.  **Run V2 Dev Server (Optional):**
    ```bash
    cd frontend_v2
    npm install
    npm run dev
    ```
4.  **Run Demo App:** `streamlit run demo_app_v2.py`

---

## 🔧 Troubleshooting

- **`RuntimeWarning: Frontend ... build directory not found`**: This means you haven't built the frontend assets yet. Run `./build_script.sh` from the root of the repository to build them.
- **Image Processing Errors on Windows**: If you encounter errors related to MIME type detection for images on Windows, it may be because the `python-magic` library is not installed or configured correctly. This component has a fallback mechanism, but for full support, you may need to install `python-magic-bin`.
- **Component fails to load model**: The component downloads models from Hugging Face Hub at runtime. If you are in an environment with no internet access, the component will fail to load new models. Ensure you have a stable internet connection.

---

## 💻 Browser Compatibility

This component relies on [WebAssembly](https://webassembly.org/) to run the `transformers.js` library directly in the browser. It is compatible with all modern browsers that have WebAssembly support, including:

- Google Chrome (Desktop and Mobile)
- Mozilla Firefox (Desktop and Mobile)
- Apple Safari (Desktop and Mobile)
- Microsoft Edge

Internet Explorer is **not** supported.

---

## 🚀 Performance Notes

- **Model Loading**: The first time you use a model, it needs to be downloaded from the Hugging Face Hub. This can take some time, especially for large models. Subsequent uses will be much faster as the model will be cached by the browser.
- **Inference Time**: The speed of the model depends on the complexity of the model and the hardware of the user's machine. Larger models will take longer to run, and performance will vary between desktop and mobile devices.
- **Hardware Acceleration**: `Transformers.js` can leverage hardware acceleration (e.g., WebGPU) if available, which can significantly improve performance.

---

## ☁️ Stlite and Streamlit Cloud

This component is fully compatible with both `stlite` (Pyodide) and Streamlit Cloud. Because all models run in the browser, there are no special server-side dependencies or configurations required. This makes it an ideal choice for serverless deployments.

---
*For legacy V1 examples, license, and contribution guidelines, see the original documentation sections.*
