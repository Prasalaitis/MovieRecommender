import psycopg2
import logging
from contextlib import contextmanager
from typing import Dict, Iterator, Any


class DatabaseConnection:
    """
    Manages the database connections. It ensures that connections are properly opened and
    closed, and transactions are correctly managed with commits or rollbacks as needed.
    """

    def __init__(self, db_config: Dict[str, Any]):
        """
        Initializes the DatabaseConnection with the provided database configuration.

        :param db_config: A dictionary containing the database connection parameters.
        """
        self.db_config = db_config

    @contextmanager
    def connect(self) -> Iterator[psycopg2.extensions.connection]:
        """
        A context manager that manages a database connection. It automatically commits
        the transaction on successful block execution or rolls back if an exception occurs.

        :yield: The database connection object to be used within a `with`-statement block.
        """
        connection: psycopg2.extensions.connection = None
        try:
            connection = psycopg2.connect(**self.db_config)
            yield connection
        except psycopg2.DatabaseError as e:
            logging.error(f"Database error: {e}")
            if connection is not None:
                connection.rollback()
            raise
        finally:
            if connection is not None:
                connection.close()
