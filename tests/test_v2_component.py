import unittest
from unittest.mock import patch

from st_transformers_js import transformers_js_pipeline_v2

class TestComponentV2(unittest.TestCase):

    @patch('st_transformers_js.v2._component_func')
    def test_v2_component_call(self, mock_component_func):
        """
        Test that the v2 component is called with the correct arguments.
        """
        # Arrange
        model_name = "test-model"
        pipeline_type = "text-classification"
        inputs = "Hello, v2!"
        config = {"a": 1}

        # Act
        transformers_js_pipeline_v2(
            model_name=model_name,
            pipeline_type=pipeline_type,
            inputs=inputs,
            config=config,
            key="test_v2"
        )

        # Assert
        expected_data = {
            "model_name": model_name,
            "pipeline_type": pipeline_type,
            "inputs": inputs,
            "mime_type": None,
            "config": config,
        }
        mock_component_func.assert_called_once_with(data=expected_data, key="test_v2")

if __name__ == '__main__':
    unittest.main()
