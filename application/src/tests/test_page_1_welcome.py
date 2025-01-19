import unittest
from unittest.mock import MagicMock, patch
from streamlit_app_folder.page_1_welcome import welcome_text, image_with_motivation  # Replace with your module name


class TestStreamlitFunctions(unittest.TestCase):

    @patch("streamlit_app_folder.page_1_welcome.st")
    def test_welcome_text(self, mock_st):
        """Test the `welcome_text` function."""
        # Simulate session state
        mock_st.session_state = {"name": "Test User"}

        # Call the function
        welcome_text()

        # Verify the header and write calls
        mock_st.header.assert_called_once_with("Welcome *Test User*")
        mock_st.write.assert_called_once_with(
            "We are grateful for your selection of our services and will do our best to assist you in your search."
        )

    ## Sadly not working: Mock cannot call st.container properly. 
    ## Even with specifing st.columns or leaving columns out of the test.
    
    # @patch("streamlit_app_folder.page_1_welcome.st")
    # def test_image_with_motivation(self, mock_st):
    #     """Test the `image_with_motivation` function."""
    #     # Mock container and columns
    #     mock_container = MagicMock()
    #     mock_col1 = MagicMock()
    #     mock_col2 = MagicMock()

    #     # Mock the container context manager
    #     mock_st.container.return_value.__enter__.return_value = mock_container

    #     # Mock columns to return two objects
    #     mock_st.columns.return_value = (mock_col1, mock_col2)

    #     # Call the function
    #     image_with_motivation()

    #     # Verify container header is called
    #     mock_container.header.assert_called_once_with("Let's create the future")
    #     mock_st.columns.assert_called_once_with(2)  # Ensure st.columns(2) is called
    #     mock_col1.image.assert_called_once_with("data/Ai_pic_berlin_for_welcome.jpeg")
    #     mock_col2.image.assert_called_once_with("data/Ai_pic_berlin_for_welcome2.jpeg")
    #     mock_container.write.assert_called_once_with(
    #         "Berlin as it should be. And with your help, we are already one step closer."
    #     )




if __name__ == "__main__":
    unittest.main()
