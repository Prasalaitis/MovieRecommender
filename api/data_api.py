import pandas as pd
import logging
from sqlalchemy import create_engine
from database.database_connection import DatabaseConnection
from psycopg2 import OperationalError, DataError


class DataAPI:
    """
    Provides an interface for performing database operations such as
    selecting data, updating data, performing administrative queries, and
    loading data into the database from a DataFrame.
    """

    def __init__(self, db_config):
        """
        Initializes the DataAPI with database configuration settings
        """
        self.db_connection = DatabaseConnection(db_config)
        self.engine = create_engine(
            f"postgresql+psycopg2://"
            f"{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
        )

    def select_data(self, query: str) -> pd.DataFrame:
        """
        Selects data from the database. Returns a DataFrame.
        """
        try:
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            raise

    def update_data(self, query: str, params=None) -> None:
        """
        Executes DML queries
        """
        try:
            with self.db_connection.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    rows_affected = cursor.rowcount
                    conn.commit()
                    logging.info(
                        f"Query executed successfully: {query} - Rows affected: {rows_affected}"
                    )
        except (OperationalError, DataError) as e:
            logging.error(f"Error updating data: {e}")
            raise

    def administrative_query(self, query: str, params=None) -> None:
        """
        Executes administrative queries such as permissions & constraints.
        """
        try:
            with self.db_connection.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    conn.commit()
                    logging.info(f"Admin query executed successfully: {query}")
        except (OperationalError, DataError) as e:
            logging.error(f"Error executing admin query: {e}")
            raise

    def load_data_to_db(self, dataframe: pd.DataFrame, table_name: str) -> None:
        """
        Loads data from a DataFrame into the specified table in the database.
        """
        try:
            logging.info(f"Starting to load data into {table_name}")
            dataframe.to_sql(table_name, self.engine, if_exists="replace", index=False)
            logging.info(f"Data loaded successfully into {table_name}")
        except Exception as e:
            logging.error(f"Error loading data to database: {e}")
            raise
