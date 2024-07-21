import logging
import argparse
import pandas as pd
from psycopg2 import OperationalError, DataError
from config.logging_config import setup_logging
from config.db_setup import db_config
from api.data_api import DataAPI


class Netflix:
    """
    This class provides functionality to interact with Netflix data using a command-line interface.
    It allows for executing SQL queries and displaying the results.
    """

    def __init__(self):
        self.api = DataAPI(db_config)
        setup_logging()

    def execute_sql(self, query):
        """
        Executes a SQL query using the DataAPI. SELECT queries return a DataFrame,
        while other queries return a status message.

        :param query: The SQL query to be executed.
        :return: Either a DataFrame (for SELECT queries) or a status message string.
        """
        try:
            if query.lower().startswith("select"):
                data = self.api.select_data(query)
                return data if not data.empty else "No data found."
            else:
                rows_affected = self.api.update_data(query)
                return f"Query executed successfully - Rows affected: {rows_affected}"
        except (OperationalError, DataError) as db_err:
            logging.error(f"Database error executing query: {db_err}")
            return "A database error occurred. Please check the logs for details."
        except Exception as e:
            logging.error(f"Unexpected error executing query: {e}")
            return "An unexpected error occurred. Please check the logs for details."

    def analyze(self):
        """
        Parses the command line arguments for a SQL query and executes it,
        then prints the result. DataFrames are printed in a readable format.
        """
        parser = argparse.ArgumentParser(
            description="Netflix Data API Command Line Tool"
        )
        parser.add_argument("sql_query", help="SQL query to execute")
        args = parser.parse_args()

        result = self.execute_sql(args.sql_query)
        if isinstance(result, pd.DataFrame):
            print(result.to_string(index=False))  # Pretty print the DataFrame
        else:
            print(result)


if __name__ == "__main__":
    analyzer = Netflix()
    analyzer.analyze()
