import unittest
from recommender.recommender import MoviesRecommender
from unittest.mock import MagicMock, patch
import pandas as pd


class TestMoviesRecommender(unittest.TestCase):
    """
    It verifies that the recommendations are generated and recorded correctly.
    """

    def setUp(self):
        """
        This initializes a MagicMock to mock the DataAPI and creates an instance of
        MoviesRecommender with the mocked API.
        """
        self.api_mock = MagicMock()
        self.recommender = MoviesRecommender(self.api_mock)

    def test_get_random_recommendation(self):
        """
        Test case to verify that get_random_recommendation method returns a random
        recommendation from the list of movies. It mocks the selection of random movies
        to control the output.
        """
        # Mock the API select_data method to return a DataFrame with the correct column name
        mock_df = pd.DataFrame({"TITLE": ["Inception", "Forrest Gump"]})
        self.api_mock.select_data.return_value = mock_df

        with patch("random.choice", return_value="Inception"):
            recommendation = self.recommender.get_random_recommendation()
            self.assertEqual(recommendation, "Inception")

    def test_record_recommendation(self):
        """
        Test case to ensure that record_recommendation method correctly records a
        recommendation in the database. It verifies the SQL query and parameters used.
        """
        # Test recording a recommendation
        self.recommender.record_recommendation("Inception")
        # Ensure the SQL query matches the actual command used
        expected_query = "INSERT INTO recommendations (title) VALUES (%s)"
        self.api_mock.update_data.assert_called_once_with(
            expected_query, ("Inception",)
        )


if __name__ == "__main__":
    unittest.main()
