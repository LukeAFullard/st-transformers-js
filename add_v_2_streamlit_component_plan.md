# Add V2 Streamlit Component Plan

## Goal
Add a **Streamlit Component v2 module** alongside the existing v1 module to maintain **forward and backward compatibility**. The project will expose both APIs under the same package, enabling developers to choose their preferred version.

---

## Folder Structure
```
st-transformers-js/
├── st_transformers_js/
│   ├── __init__.py              # Exposes both v1 and v2
│   ├── v1.py                    # Current implementation
│   ├── v2.py                    # New v2 module
│   ├── frontend_v1/             # Existing frontend
│   └── frontend_v2/             # New React/TypeScript frontend
├── frontend_v2/                 # Root-level source for v2 development
│   ├── package.json
│   ├── tsconfig.json
│   ├── src/
│   │   ├── index.tsx
│   │   └── StreamlitBridge.ts
│   └── public/
│       └── index.html
├── demo_app_v2.py               # Demonstration app for v2
├── setup.py
├── MANIFEST.in
└── tests/
    ├── test_v1_component.py
    └── test_v2_component.py
```

---

## Implementation Plan

### 1. Create `v2.py`
Use the new Streamlit Components API (v2). Example:

```python
import os
import streamlit.components.v2 as components

_component_func = components.declare_component(
    name="st_transformers_js_v2",
    path=os.path.join(os.path.dirname(__file__), "frontend_v2/build"),
)

def st_transformers_js_v2(**kwargs):
    return _component_func(**kwargs)
```

### 2. Modify `__init__.py`
Expose both versions under a single namespace:

```python
from .v1 import st_transformers_js as st_transformers_js_v1
from .v2 import st_transformers_js_v2

__all__ = ["st_transformers_js_v1", "st_transformers_js_v2"]
```

### 3. Create React/TypeScript Frontend (v2)
Set up a modern React + TypeScript app using `create-react-app` or Vite. Use `@streamlit/components-v2`.

Example `src/index.tsx`:
```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { StreamlitProvider, withStreamlitConnection } from "@streamlit/components-v2";

function App({ args }) {
  return <div>Transformer output: {args?.text}</div>;
}

const StreamlitApp = withStreamlitConnection(App);
const root = ReactDOM.createRoot(document.getElementById("root")!);
root.render(
  <StreamlitProvider>
    <StreamlitApp />
  </StreamlitProvider>
);
```

### 4. Add Demo App for v2
```python
import streamlit as st
from st_transformers_js import st_transformers_js_v2

st.title("st-transformers-js v2 Demo")
response = st_transformers_js_v2(text="Hello v2!")
st.write("Response:", response)
```

### 5. Testing Plan
- **Unit tests:** ensure both v1 and v2 components import correctly.
- **Smoke tests:** run both demo apps.
- **Visual tests:** confirm the v2 frontend displays correctly.

```python
from st_transformers_js import st_transformers_js_v2

def test_v2_import():
    assert callable(st_transformers_js_v2)
```

---

## Packaging and Distribution

### MANIFEST.in
```
recursive-include st_transformers_js/frontend_v1 *
recursive-include st_transformers_js/frontend_v2/build *
```

### setup.py
Ensure both builds are included:
```python
setup(
    ...,
    include_package_data=True,
    packages=find_packages(),
    package_data={
        'st_transformers_js': ['frontend_v1/*', 'frontend_v2/build/*']
    },
)
```

### pyproject.toml (optional modernization)
Add build system requirements for modern packaging:
```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

---

## Release Checklist

### Pre-Release
1. ✅ Verify both v1 and v2 function independently.
2. ✅ Ensure demo apps render correctly in Streamlit.
3. ✅ Update README.md with new import examples.
4. ✅ Increment `setup.py` version number.
5. ✅ Run packaging tests:
   ```bash
   python setup.py sdist bdist_wheel
   twine check dist/*
   ```
6. ✅ Build v2 frontend:
   ```bash
   cd frontend_v2 && npm install && npm run build
   ```

### PyPI Release
```bash
python -m twine upload dist/*
```

### Post-Release
- [ ] Update documentation site with both examples.
- [ ] Add badges to README: PyPI version, Streamlit compatibility.
- [ ] Create GitHub tag and release notes summarizing dual support.
- [ ] Announce on Streamlit forums.

---

## Future Enhancements
- Add TypeScript typings for JS↔️Python data schema.
- Implement event callbacks for dynamic updates.
- Integrate automated visual regression tests (e.g., Playwright).
- Add a build verification GitHub Action.
- Provide migration guide from v1 → v2.

---

## Next Actions
1. Scaffold the `frontend_v2/` directory with CRA or Vite.
2. Add a basic React+TS component using `@streamlit/components-v2`.
3. Build once to produce `/build/`.
4. Implement `v2.py` loader.
5. Update `__init__.py` and tests.
6. Verify end-to-end in demo apps.
7. Release version `0.2.0` with dual v1/v2 support.