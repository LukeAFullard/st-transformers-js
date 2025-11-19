import unittest
from unittest.mock import patch, MagicMock, ANY
import base64

# Mock streamlit before import
mock_streamlit = MagicMock()
mock_streamlit.components.v2.component.return_value = MagicMock()

modules = {
    "streamlit": mock_streamlit,
    "streamlit.components.v2": mock_streamlit.components.v2,
}

with patch("os.path.exists", return_value=True):
    with patch.dict("sys.modules", modules):
        from st_transformers_js import v2 as transformers_v2

class TestComponentV2(unittest.TestCase):

    def setUp(self):
        self.component_func_patcher = patch("st_transformers_js.v2._component_func")
        self.mock_component_func = self.component_func_patcher.start()

    def tearDown(self):
        self.component_func_patcher.stop()

    def test_v2_component_call(self):
        """
        Test that the v2 component is called with the correct arguments.
        """
        model_name = "test-model"
        pipeline_type = "text-classification"
        inputs = "Hello, v2!"
        config = {"a": 1}

        transformers_v2.transformers_js_pipeline_v2(
            model_name=model_name,
            pipeline_type=pipeline_type,
            inputs=inputs,
            config=config,
            key="test_v2",
        )

        expected_data = {
            "model_name": model_name,
            "pipeline_type": pipeline_type,
            "inputs": inputs,
            "mime_type": None,
            "config": config,
        }
        self.mock_component_func.assert_called_once_with(
            data=expected_data,
            key="test_v2",
        )

    def test_v2_image_input(self):
        """Test that image byte inputs are correctly processed and passed to the component."""
        mock_magic = MagicMock()
        mock_magic.from_buffer.return_value = "image/png"

        with patch.dict('sys.modules', {'magic': mock_magic}):
            img_bytes = b"fake-image-bytes"
            expected_b64_str = base64.b64encode(img_bytes).decode("utf-8")

            transformers_v2.transformers_js_pipeline_v2(
                model_name="test-model",
                pipeline_type="image-to-text",
                inputs=img_bytes,
                key="test_img_v2",
            )

            expected_data = {
                "model_name": "test-model",
                "pipeline_type": "image-to-text",
                "inputs": expected_b64_str,
                "mime_type": "image/png",
                "config": {},
            }

            self.mock_component_func.assert_called_once_with(
                data=expected_data,
                key="test_img_v2",
            )

if __name__ == '__main__':
    unittest.main()
