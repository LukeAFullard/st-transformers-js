# st-transformers-js

A fully **offline Streamlit component** for running Hugging Face Transformers.js models in the browser. Works seamlessly with Streamlit Cloud, stlite, and Pyodide environments.

## ✨ Features

- 🔌 **Fully Offline** - Bundles transformers.js locally, no CDN dependencies
- 🚀 **Zero Backend** - Models run entirely in the browser via WebAssembly
- 🎯 **All Pipeline Types** - Supports image-to-text, text classification, token classification, and more
- 📦 **Version Locked** - Reproducible builds with locked transformers.js version
- 🌐 **stlite Compatible** - Works in Pyodide/WASM environments
- 🎨 **Progress Logging** - Visual feedback during model loading and inference

## 📦 Installation

```bash
pip install st-transformers-js
```

## 🚀 Quick Start

### Image to Text (Donut)

```python
import streamlit as st
from st_transformers_js import transformers_js_pipeline

st.title("Document OCR with Donut")

uploaded_file = st.file_uploader("Upload a receipt or document", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img_bytes = uploaded_file.read()
    st.image(img_bytes, caption="Uploaded Image", width=300)
    
    with st.spinner("Processing..."):
        result = transformers_js_pipeline(
            model_name="Xenova/donut-base-finetuned-cord-v2",
            pipeline_type="image-to-text",
            inputs=img_bytes
        )
    
    if result:
        st.json(result)
```

### Text Classification

```python
import streamlit as st
from st_transformers_js import transformers_js_pipeline

text = st.text_area("Enter text to classify:", "I love this product!")

if st.button("Classify"):
    result = transformers_js_pipeline(
        model_name="Xenova/distilbert-base-uncased-finetuned-sst-2-english",
        pipeline_type="text-classification",
        inputs=text
    )
    
    if result:
        st.write(f"**Label:** {result[0]['label']}")
        st.write(f"**Confidence:** {result[0]['score']:.2%}")
```

### Token Classification (NER)

```python
import streamlit as st
from st_transformers_js import transformers_js_pipeline

text = st.text_area("Enter text for NER:", "My name is Sarah and I live in London.")

if st.button("Extract Entities"):
    result = transformers_js_pipeline(
        model_name="Xenova/bert-base-NER",
        pipeline_type="token-classification",
        inputs=text,
        config={"aggregation_strategy": "simple"}
    )
    
    if result:
        for entity in result:
            st.write(f"**{entity['word']}** - {entity['entity_group']} ({entity['score']:.2%})")
```

## 🎯 Supported Pipelines

The component supports all Transformers.js pipeline types:

- `image-to-text` - Document OCR, image captioning
- `text-classification` - Sentiment analysis, topic classification
- `token-classification` - Named entity recognition (NER)
- `question-answering` - Extract answers from context
- `summarization` - Text summarization
- `translation` - Language translation
- `text-generation` - Text completion
- `zero-shot-classification` - Classify without training
- And more...

## 📖 API Reference

### `transformers_js_pipeline()`

```python
transformers_js_pipeline(
    model_name: str,
    pipeline_type: str,
    inputs: Union[str, bytes, dict],
    config: Optional[dict] = None,
    width: int = 600,
    height: int = 400,
    key: Optional[str] = None
) -> Optional[dict]
```

**Parameters:**

- `model_name` (str): Hugging Face model identifier (e.g., "Xenova/donut-base-finetuned-cord-v2")
- `pipeline_type` (str): Pipeline type (e.g., "image-to-text", "text-classification")
- `inputs` (str | bytes | dict): Input data (text string, image bytes, or structured input)
- `config` (dict, optional): Additional pipeline configuration
- `width` (int): Component width in pixels (default: 600)
- `height` (int): Component height in pixels (default: 400)
- `key` (str, optional): Unique component key for Streamlit

**Returns:**
- `dict | None`: Pipeline output as JSON, or None if still processing

## 🛠️ Development Setup

### Project Structure

```
st_transformers_js/
│
├─ frontend/
│   ├─ public/
│   │   ├─ index.html
│   │   └─ transformers.min.js   ← Download from CDN
│   └─ build/                     ← Created during build
│
├─ st_transformers_js/
│   └─ __init__.py
│
├─ setup.py
├─ pyproject.toml
├─ MANIFEST.in
└─ README.md
```

### Setup Instructions

1. **Download transformers.min.js**

Download the bundled version from:
```
https://cdn.jsdelivr.net/npm/@xenova/transformers@3.2.0/dist/transformers.min.js
```

Place it in `frontend/public/transformers.min.js`

2. **Prepare the build directory**

```bash
# Create build directory
mkdir -p st_transformers_js/frontend/build

# Copy files to build
cp frontend/public/* st_transformers_js/frontend/build/
```

3. **Install in development mode**

```bash
pip install -e .
```

4. **Test the component**

```bash
streamlit run demo_app.py
```

## 📦 Building for Distribution

```bash
# Build the package
python -m build

# Upload to PyPI
pip install --upgrade twine
twine upload dist/*
```

## 🔄 Version Updates

To update the transformers.js version:

1. Download new `transformers.min.js` from CDN
2. Replace in `frontend/public/`
3. Increment version in `setup.py` and `pyproject.toml`
4. Rebuild and test
5. Publish new version

## 🌐 stlite / Pyodide Compatibility

This component is fully compatible with:
- **stlite** - Streamlit in the browser via Pyodide
- **Streamlit Cloud** - Standard cloud deployment
- **Local Streamlit** - Traditional Python environment

The offline bundle ensures models load without network dependencies after initial download.

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 🐛 Issues

Report bugs and request features at:
https://github.com/yourusername/st-transformers-js/issues

## 🙏 Acknowledgments

Built on top of:
- [Transformers.js](https://github.com/xenova/transformers.js) by Xenova
- [Streamlit](https://streamlit.io/)
- [Hugging Face](https://huggingface.co/)

---

Made with ❤️ for the Streamlit community
