from api.data_api import DataAPI
from config.db_setup import db_config
from config.logging_config import setup_logging
from scripts.data_loader import DataLoader
from scripts.constraints import DatabaseConstraints
from scripts.permissions import DatabasePermissions


class DataPipeline:
    """
    This class represents the main data pipeline for setting up the database,
    loading data, and configuring database constraints and permissions.
    """

    def __init__(self, api: DataAPI):
        """
        Initialize the DataPipeline with an instance of the DataAPI.

        :param api: An instance of DataAPI to interact with the database.
        """
        self.api = api

    def setup_logging(self) -> None:
        """Set up logging for the application."""
        setup_logging()

    def load_data(self) -> None:
        """
        Load data into the database using DataLoader.
        """
        loader = DataLoader(self.api)
        loader.load_csv_to_db()

    def setup_database_constraints(self) -> None:
        """
        Set up database constraints using DatabaseConstraints.
        """
        db_constraints = DatabaseConstraints(self.api)
        db_constraints.setup_constraints()

    def setup_database_permissions(self) -> None:
        """
        Set up database permissions using DatabasePermissions.
        """
        db_permissions = DatabasePermissions(self.api)
        db_permissions.setup_permissions()

    def run_pipeline(self) -> None:
        """
        Run the full data pipeline: setup logging, load data, set up constraints,
        and permissions in sequence.
        """
        self.setup_logging()
        self.load_data()
        self.setup_database_constraints()
        self.setup_database_permissions()


def main() -> None:
    """
    The main function that creates an instance of the data pipeline and runs it.
    """
    # Initialize the Data API
    api = DataAPI(db_config)

    # Create an instance of the data pipeline and run it
    data_pipeline = DataPipeline(api)
    data_pipeline.run_pipeline()


if __name__ == "__main__":
    main()
