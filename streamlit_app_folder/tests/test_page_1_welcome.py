from unittest.mock import patch, call
import unittest

class TestStreamlitApp(unittest.TestCase):
    @patch('streamlit.header')
    @patch('streamlit.write')
    def test_welcome_text(self, mock_write, mock_header):
        from page_1_welcome import welcome_text  # Import the function to test

        with patch('streamlit.session_state', {'name': 'Alice'}):
            welcome_text()

        # Verify header was called with the correct text
        mock_header.assert_called_once_with('Welcome *Guest*')

        # Verify write was called with the correct text
        mock_write.assert_called_once_with(
            'We are grateful for your selection of our services and will do our best to assist you in your search.'
        )

    # @patch('streamlit.container')
    # @patch('streamlit.columns')
    # @patch('streamlit.image')
    # @patch('streamlit.header')
    # @patch('streamlit.write')
    # def test_image_with_motivation(self, mock_write, mock_header, mock_image, mock_columns, mock_container):
    #     from page_1_welcome import image_with_motivation  # Import the function to test

    #     # Mock the columns to return two mock objects
    #     mock_col1 = unittest.mock.Mock()
    #     mock_col2 = unittest.mock.Mock()
    #     mock_columns.return_value = (mock_col1, mock_col2)

    #     image_with_motivation()

    #     # Verify header was called with the correct text
    #     mock_header.assert_called_once_with("Let's create the future")

    #     # Verify images were displayed in columns
    #     mock_image.assert_any_call("data/Ai_pic_berlin_for_welcome.jpeg")
    #     mock_image.assert_any_call("data/Ai_pic_berlin_for_welcome2.jpeg")

    #     # Verify write was called with the motivational message
    #     mock_write.assert_called_once_with(
    #         "Berlin as it should be. And with your help, we are already one step closer."
    #     )

    # @patch('main.welcome_text')
    # @patch('main.image_with_motivation')
    # def test_main_function(self, mock_image_with_motivation, mock_welcome_text):
    #     from page_1_welcome import main  # Import the function to test

    #     main()

    #     # Verify that the main function calls the other two functions
    #     mock_welcome_text.assert_called_once()
    #     mock_image_with_motivation.assert_called_once()

if __name__ == "__main__":
    unittest.main()
