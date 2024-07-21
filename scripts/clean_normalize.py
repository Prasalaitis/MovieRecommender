import pandas as pd
from pathlib import Path
import logging
from config.logging_config import setup_logging
from typing import Dict, Any, Tuple


class DataNormalizer:
    """
    This class is responsible for normalizing and cleaning data related to raw titles and credits.
    It reads data from CSV files, processes the data, and prepares it for database insertion.
    """

    def __init__(self, titles_filename, credits_filename):
        """
        :param titles_filename: The filename of the titles data CSV.
        :param credits_filename: The filename of the credits data CSV.
        """
        self.script_directory = Path(__file__).parent
        self.titles_path = self.script_directory / f"../data/{titles_filename}"
        self.credits_path = self.script_directory / f"../data/{credits_filename}"

    def load_csv(self, file_path: Path) -> pd.DataFrame:
        """
        Loads a CSV file into a pandas DataFrame.
        """
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            raise
        except Exception as e:
            logging.error(f"Error loading file: {e}")
            raise

    def clean_characters(self, characters: str) -> list:
        """
        Cleans a string of characters by replacing certain separators and returns a list of characters.

        :param characters: A string containing characters separated by slashes or semicolons.
        :return: A list of cleaned character strings.
        """
        if pd.isna(characters):
            return []
        characters = characters.replace(" / ", "/").replace(";", "/")
        return [char.strip() for char in characters.split("/")]

    def extract_column(self, df: pd.DataFrame, column_name: str) -> pd.Series:
        """
        Extracts and cleans a column from a DataFrame that contains string representations of lists.

        :param df: The DataFrame to process.
        :param column_name: The name of the column to extract.
        :return: A pandas Series with the cleaned list-like data.
        """
        return df[column_name].str.strip("[]").str.replace("'", "").str.split(", ")

    def normalize_credits(
        self, credits_df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Normalizes the credits data by creating a separate DataFrame for characters.

        :param credits_df: The DataFrame containing credits data.
        :return: A tuple containing the normalized credits DataFrame and the characters DataFrame.
        """
        characters_list = (
            credits_df["character"].apply(self.clean_characters).explode().unique()
        )
        characters_df = pd.DataFrame(
            characters_list, columns=["character_name"]
        ).dropna()
        characters_df.reset_index(drop=True, inplace=True)
        characters_df.index += 1
        characters_df["character_id"] = characters_df.index

        credits_exploded = credits_df.assign(
            character=credits_df["character"].apply(self.clean_characters)
        ).explode("character")
        credits_df = pd.merge(
            credits_exploded,
            characters_df,
            left_on="character",
            right_on="character_name",
            how="left",
        )
        credits_df = credits_df.dropna(subset=["character_id"])
        credits_df["character_id"] = credits_df["character_id"].astype(int)
        credits_df.drop(["index", "character", "character_name"], axis=1, inplace=True)
        credits_df = credits_df.drop_duplicates()

        return credits_df, characters_df

    def normalize_titles(
        self, titles_df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Normalizes the titles data by creating separate DataFrames for genres and production countries.

        :param titles_df: The DataFrame containing titles data.
        :return: A tuple containing the normalized titles DataFrame, genres DataFrame,
                 countries DataFrame, movie_genres DataFrame, and movie_countries DataFrame.
        """
        titles_df["genres"] = self.extract_column(titles_df, "genres")
        titles_df["production_countries"] = self.extract_column(
            titles_df, "production_countries"
        )

        # Normalizing genres with genre_id
        genres_df = (
            pd.DataFrame(titles_df["genres"].explode().unique(), columns=["genre"])
            .dropna()
            .reset_index(drop=True)
        )
        genres_df.index += 1
        genres_df["genre_id"] = genres_df.index

        # Normalizing countries with country_id
        countries_df = (
            pd.DataFrame(
                titles_df["production_countries"].explode().unique(),
                columns=["country"],
            )
            .dropna()
            .reset_index(drop=True)
        )
        countries_df.index += 1
        countries_df["country_id"] = countries_df.index

        # Normalizing relationship tables with new ids
        movie_genres_df = titles_df.explode("genres")[["id", "genres"]]
        movie_genres_df = movie_genres_df.merge(
            genres_df, left_on="genres", right_on="genre", how="left"
        )[["id", "genre_id"]]

        movie_countries_df = titles_df.explode("production_countries")[
            ["id", "production_countries"]
        ]
        movie_countries_df = movie_countries_df.merge(
            countries_df, left_on="production_countries", right_on="country", how="left"
        )[["id", "country_id"]]

        movies_df = titles_df.drop(["index", "genres", "production_countries"], axis=1)
        movies_df = movies_df.drop_duplicates()

        return movies_df, genres_df, countries_df, movie_genres_df, movie_countries_df

    def _recommendations_table(self) -> pd.DataFrame:
        """
        Creates an empty DataFrame for recommendations data with predefined columns.
        :return: An empty recommendations DataFrame.
        """
        recommendations_df = pd.DataFrame(
            columns=["recommendation_id", "title", "datestamp"]
        )
        return recommendations_df

    def process_and_save_data(self) -> Dict[str, pd.DataFrame]:
        """
        Processes and normalizes titles and credits data, then returns it in a dictionary of DataFrames.
        :return: A dictionary containing DataFrames for movies, genres, countries,
                 movie_genres, movie_countries, credits, characters, and recommendations.
        """
        titles_df = self.load_csv(self.titles_path)
        credits_df = self.load_csv(self.credits_path)

        movies_df, genres_df, countries_df, movie_genres_df, movie_countries_df = (
            self.normalize_titles(titles_df)
        )
        credits_df, characters_df = self.normalize_credits(credits_df)
        recommendations_df = self._recommendations_table()

        return {
            "movies": movies_df,
            "genres": genres_df,
            "countries": countries_df,
            "movie_genres": movie_genres_df,
            "movie_countries": movie_countries_df,
            "credits": credits_df,
            "characters": characters_df,
            "recommendations": recommendations_df,
        }


if __name__ == "__main__":
    setup_logging()
    normalizer = DataNormalizer("raw_titles.csv", "raw_credits.csv")
    normalizer.process_and_save_data()
