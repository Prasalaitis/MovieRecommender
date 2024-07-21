import pandas as pd
from pathlib import Path
import logging
from api.data_api import DataAPI
from config.db_setup import db_config
from scripts.clean_normalize import DataNormalizer


class DataLoader:
    """
    DataLoader is responsible for loading data from CSV files into the database.
    It uses a DataNormalizer to process raw data and then uploads the resulting clean data.
    """

    def __init__(self, api):
        self.api = api
        normalizer = DataNormalizer("raw_titles.csv", "raw_credits.csv")
        normalized_dataframes = (
            normalizer.process_and_save_data()
        )  # Get processed dataframes

        self.dataframes = {
            "best_movies": "Best Movies Netflix.csv",
        }

        self.load_additional_data()  # Load additional CSV data
        self.dataframes.update(normalized_dataframes)  # Merge with normalized data

    def load_additional_data(self) -> None:
        """
        Loads additional data from CSV files specified in the self.dataframes dictionary
        """
        for key, filename in self.dataframes.items():
            try:
                path = Path(__file__).parent / f"../data/{filename}"
                df = pd.read_csv(path)
                self.dataframes[key] = df
                logging.info(f"Loaded {filename} successfully.")
            except FileNotFoundError as e:
                logging.error(f"Error loading {filename}: {e}")
                self.dataframes[key] = pd.DataFrame()
            except Exception as e:
                logging.error(f"Unexpected error loading {filename}: {e}")

    def load_csv_to_db(self) -> None:
        """
        Iterates over the dataframes dictionary and loads each DataFrame into the database
        using the DataAPI's load_data_to_db method.
        """
        for key, df in self.dataframes.items():
            if isinstance(df, pd.DataFrame):
                try:
                    self.api.load_data_to_db(df, key)
                    logging.info(f"Successfully loaded data into '{key}' table.")
                except Exception as e:
                    logging.error(f"Failed to load data into '{key}': {e}")


if __name__ == "__main__":
    api = DataAPI(db_config)
    loader = DataLoader(api)
    loader.load_csv_to_db()
