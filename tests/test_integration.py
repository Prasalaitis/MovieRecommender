import unittest
from api.data_api import DataAPI
from config.db_setup import db_config


class TestDataAPI(unittest.TestCase):
    """
    Integration test suite for testing the DataAPI class
    """

    def setUp(self):
        """
        Creates an instance of the DataAPI to be used in the tests.
        """
        self.api = DataAPI(db_config)

    def test_update_data(self):
        """
        It performs an INSERT operation and then SELECTs the data to ensure it was inserted.
        """
        with self.api.db_connection.connect() as conn:
            cursor = conn.cursor()

            # Start a transaction
            cursor.execute("BEGIN;")

            try:
                # Perform the test DML operation
                cursor.execute(
                    "INSERT INTO recommendations (title) VALUES ('Test Movie');"
                )

                # Optionally retrieve data to verify the operation
                cursor.execute(
                    "SELECT * FROM recommendations WHERE title = 'Test Movie';"
                )
                rows = cursor.fetchall()
                self.assertTrue(len(rows) > 0)

                # Roll back the transaction to avoid permanent changes
                cursor.execute("ROLLBACK;")

            except Exception as e:
                # If there is an error, rollback the transaction
                cursor.execute("ROLLBACK;")
                raise e


if __name__ == "__main__":
    unittest.main()
