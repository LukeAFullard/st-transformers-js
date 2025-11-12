import unittest
from unittest.mock import patch
from st_transformers_js.v2 import st_transformers_js_v2

class TestComponentV2(unittest.TestCase):

    @patch('st_transformers_js.v2.components.component')
    def test_v2_component_call(self, mock_component):
        """
        Test that the v2 component is called with the correct arguments.
        """
        # Arrange
        mock_component_func = mock_component.return_value
        test_text = "Hello, v2!"

        # Act
        st_transformers_js_v2(text=test_text, key="test_v2")

        # Assert
        mock_component_func.assert_called_once_with(text=test_text, key="test_v2", default=None)

if __name__ == '__main__':
    unittest.main()
