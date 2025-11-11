import unittest
import base64
from unittest.mock import patch
from st_transformers_js import transformers_js_pipeline

class TestComponent(unittest.TestCase):

    @patch('st_transformers_js._component_func')
    def test_byte_input_encoding(self, mock_component_func):
        """
        Test that byte inputs are correctly encoded to base64.
        """
        # Arrange
        test_bytes = b'test_image_bytes'
        expected_base64 = base64.b64encode(test_bytes).decode('utf-8')

        # Act
        transformers_js_pipeline(
            model_name="test_model",
            pipeline_type="image-to-text",
            inputs=test_bytes,
            key="test1"
        )

        # Assert
        mock_component_func.assert_called_once()
        # Get the keyword arguments from the call
        called_args = mock_component_func.call_args.kwargs
        # Check if the 'inputs' argument matches the expected base64 string
        self.assertEqual(called_args.get('inputs'), expected_base64)
        self.assertEqual(called_args.get('model_name'), "test_model")
        self.assertEqual(called_args.get('pipeline_type'), "image-to-text")

    @patch('st_transformers_js._component_func')
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
        self.assertEqual(called_args.get('model_name'), "test_model_2")
        self.assertEqual(called_args.get('pipeline_type'), "text-classification")

if __name__ == '__main__':
    unittest.main()
