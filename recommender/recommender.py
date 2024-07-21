from api.data_api import DataAPI
from config.db_setup import db_config
import random
from config.logging_config import setup_logging
import logging
from typing import Optional


setup_logging()


class MoviesRecommender:
    def __init__(self, api):
        self.api = api

    def get_random_recommendation(self) -> Optional[str]:
        """
        Fetches a list of movie titles and returns one at random.
        """
        try:
            # Use double quotes for the column name
            result = self.api.select_data('SELECT "TITLE" FROM best_movies')
            if not result.empty:
                return random.choice(result["TITLE"].tolist())
            else:
                logging.info("No movies found for recommendation.")
                return None
        except Exception as e:
            logging.error(f"Error fetching recommendations: {e}")
            return None

    def record_recommendation(self, title: Optional[str]) -> None:
        """
        Records a movie title as a recommendation.
        """
        try:
            if title:
                insert_query = "INSERT INTO recommendations (title) VALUES (%s)"
                self.api.update_data(insert_query, (title,))
                logging.info(f"Recorded recommendation: {title}")
            else:
                logging.warning("No title provided for recording.")
        except Exception as e:
            logging.error(f"Error recording recommendation: {e}")


if __name__ == "__main__":
    api = DataAPI(db_config)
    recommender = MoviesRecommender(api)

    recommended_title = recommender.get_random_recommendation()

    if recommended_title:
        recommender.record_recommendation(recommended_title)
