import unittest
import base64
from unittest.mock import patch, MagicMock
from st_transformers_js import transformers_js_pipeline_v1 as transformers_js_pipeline

# A minimal PNG header
PNG_HEADER = b'\x89PNG\r\n\x1a\n'
# A minimal JPEG header
JPEG_HEADER = b'\xff\xd8'

class TestComponent(unittest.TestCase):

    @patch('st_transformers_js.v1.components.declare_component')
    def test_byte_input_encoding_with_magic(self, mock_component_func):
        """
        Test that byte inputs are correctly encoded and mime_type is set by python-magic.
        """
        # Arrange
        test_bytes = PNG_HEADER + b'test_image_bytes'
        expected_base64 = base64.b64encode(test_bytes).decode('utf-8')

        mock_magic = MagicMock()
        mock_magic.from_buffer.return_value = 'image/png'

        with patch.dict('sys.modules', {'magic': mock_magic}):
            # Act
            transformers_js_pipeline(
                model_name="test_model",
                pipeline_type="image-to-text",
                inputs=test_bytes,
                key="test1"
            )

        # Assert
        mock_component_func.assert_called_once()
        called_args = mock_component_func.call_args.kwargs
        self.assertEqual(called_args.get('inputs'), expected_base64)
        self.assertEqual(called_args.get('mime_type'), "image/png")

    @patch('st_transformers_js.v1.components.declare_component')
    def test_jpeg_mime_type_fallback(self, mock_component_func):
        """
        Test that JPEG mime type is correctly identified using the fallback mechanism.
        """
        # Arrange
        test_bytes = JPEG_HEADER + b'test_image_bytes'

        with patch.dict('sys.modules', {'magic': None}):
            # Act
            transformers_js_pipeline(
                model_name="test_model",
                pipeline_type="image-to-text",
                inputs=test_bytes,
                key="test_jpeg"
            )

        # Assert
        called_args = mock_component_func.call_args.kwargs
        self.assertEqual(called_args.get('mime_type'), "image/jpeg")

    @patch('st_transformers_js.v1.components.declare_component')
    def test_string_input_passthrough(self, mock_component_func):
        """
        Test that string inputs are passed through without modification.
        """
        # Arrange
        test_string = "This is a test sentence."

        # Act
        transformers_js_pipeline(
            model_name="test_model_2",
            pipeline_type="text-classification",
            inputs=test_string,
            key="test2"
        )

        # Assert
        mock_component_func.assert_called_once()
        called_args = mock_component_func.call_args.kwargs
        self.assertEqual(called_args.get('inputs'), test_string)
        self.assertIsNone(called_args.get('mime_type'))

    def test_invalid_input_type(self):
        """
        Test that a TypeError is raised for invalid input types.
        """
        with self.assertRaises(TypeError):
            transformers_js_pipeline(
                model_name="test_model",
                pipeline_type="text-classification",
                inputs=12345,  # Invalid input type
                key="test3"
            )

if __name__ == '__main__':
    unittest.main()
