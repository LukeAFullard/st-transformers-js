import unittest
import base64
from unittest.mock import patch, MagicMock

from st_transformers_js import transformers_js_pipeline_v1 as transformers_js_pipeline
from st_transformers_js.helpers import process_inputs

# A minimal PNG header
PNG_HEADER = b'\x89PNG\r\n\x1a\n'
# A minimal JPEG header
JPEG_HEADER = b'\xff\xd8'
# A minimal GIF header
GIF_HEADER = b'GIF89a'
# A minimal BMP header
BMP_HEADER = b'BM'
# A minimal WebP header
WEBP_HEADER = b'RIFF....WEBP'

class TestV1Component(unittest.TestCase):

    @patch('st_transformers_js.v1._component_func')
    def test_string_input_passthrough(self, mock_component_func):
        """
        Test that string inputs are passed through without modification.
        """
        transformers_js_pipeline(
            model_name="test_model_2",
            pipeline_type="text-classification",
            inputs="This is a test sentence.",
            key="test2"
        )
        mock_component_func.assert_called_once()
        called_args = mock_component_func.call_args.kwargs
        self.assertEqual(called_args.get('inputs'), "This is a test sentence.")
        self.assertIsNone(called_args.get('mime_type'))

    @patch('st_transformers_js.v1._component_func')
    def test_invalid_input_type(self, mock_component_func):
        """
        Test that a TypeError is raised for invalid input types.
        """
        with self.assertRaises(TypeError):
            transformers_js_pipeline(
                model_name="test_model",
                pipeline_type="text-classification",
                inputs=12345,
                key="test3"
            )

class TestHelpers(unittest.TestCase):

    def test_process_inputs_with_magic(self):
        """
        Test that byte inputs are correctly encoded and mime_type is set by python-magic.
        """
        test_bytes = PNG_HEADER + b'test_image_bytes'
        expected_base64 = base64.b64encode(test_bytes).decode('utf-8')

        mock_magic = MagicMock()
        mock_magic.from_buffer.return_value = 'image/png'

        with patch.dict('sys.modules', {'magic': mock_magic}):
            processed_inputs, mime_type = process_inputs(test_bytes)

        self.assertEqual(processed_inputs, expected_base64)
        self.assertEqual(mime_type, "image/png")

    def test_process_inputs_fallback(self):
        """
        Test that the fallback MIME type detection works correctly.
        """
        test_cases = [
            (PNG_HEADER, 'image/png'),
            (JPEG_HEADER, 'image/jpeg'),
            (GIF_HEADER, 'image/gif'),
            (BMP_HEADER, 'image/bmp'),
            (WEBP_HEADER, 'image/webp'),
        ]

        with patch.dict('sys.modules', {'magic': None}):
            for header, expected_mime_type in test_cases:
                with self.subTest(mime_type=expected_mime_type):
                    _, mime_type = process_inputs(header)
                    self.assertEqual(mime_type, expected_mime_type)

if __name__ == '__main__':
    unittest.main()
