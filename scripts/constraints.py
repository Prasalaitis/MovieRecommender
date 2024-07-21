import logging
from api.data_api import DataAPI
from config.db_setup import db_config


class DatabaseConstraints:
    """
    This class is responsible for setting up primary and foreign key constraints
    in the database to ensure data integrity.
    """

    def __init__(self, data_api):
        self.data_api = data_api

    def setup_constraints(self) -> None:
        commands = [
            # Adding Primary Key Constraints
            "ALTER TABLE movies ADD PRIMARY KEY (id);",
            "ALTER TABLE genres ADD PRIMARY KEY (genre_id);",
            "ALTER TABLE countries ADD PRIMARY KEY (country_id);",
            "ALTER TABLE characters ADD PRIMARY KEY (character_id);",
            "ALTER TABLE best_movies ADD PRIMARY KEY (index);",
            "ALTER TABLE credits ADD PRIMARY KEY (person_id, character_id, id);",
            "ALTER TABLE movie_genres ADD PRIMARY KEY (id, genre_id);",
            "ALTER TABLE movie_countries ADD PRIMARY KEY (id, country_id);",
            # Adding Foreign Key Constraints
            "ALTER TABLE movie_genres ADD CONSTRAINT fk_movie_genres_movies FOREIGN KEY (id) REFERENCES movies (id);",
            "ALTER TABLE movie_genres ADD CONSTRAINT fk_movie_genres_genres FOREIGN KEY (genre_id) REFERENCES genres (genre_id);",
            "ALTER TABLE movie_countries ADD CONSTRAINT fk_movie_countries_movies FOREIGN KEY (id) REFERENCES movies (id);",
            "ALTER TABLE movie_countries ADD CONSTRAINT fk_movie_countries_countries FOREIGN KEY (country_id) REFERENCES countries (country_id);",
            "ALTER TABLE credits ADD CONSTRAINT fk_credits_characters_characters FOREIGN KEY (character_id) REFERENCES characters (character_id);",
            "ALTER TABLE credits ADD CONSTRAINT fk_credits_movie_movie FOREIGN KEY (id) REFERENCES movies (id);",
            # Recommendation table modifications
            "ALTER TABLE recommendations ALTER COLUMN recommendation_id SET NOT NULL;",
            "ALTER TABLE recommendations ALTER COLUMN datestamp SET DEFAULT CURRENT_TIMESTAMP;",
            "ALTER TABLE recommendations ALTER COLUMN recommendation_id TYPE INTEGER USING recommendation_id::INTEGER;",
            "ALTER TABLE recommendations ALTER COLUMN recommendation_id ADD GENERATED ALWAYS AS IDENTITY;",
            "ALTER TABLE recommendations ADD PRIMARY KEY (recommendation_id);",
        ]

        for cmd in commands:
            try:
                logging.info(f"Executing command: {cmd}")
                self.data_api.administrative_query(cmd)
                logging.info("Command executed successfully.")
            except Exception as e:
                logging.error(f"Error executing command: {e}")


if __name__ == "__main__":
    data_api = DataAPI(db_config)

    db_constraints = DatabaseConstraints(data_api)
    db_constraints.setup_constraints()
