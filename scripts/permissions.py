import logging
from api.data_api import DataAPI
from config.db_setup import db_config


class DatabasePermissions:
    """
    This class handles the setup of database roles and permissions for different types of users.
    """

    def __init__(self, data_api):
        self.data_api = data_api

    def setup_permissions(self) -> None:
        """
        Executes SQL commands to set up roles and permissions within the database.
        """
        commands = [
            # Check and create roles if they don't exist
            "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'netflix_data_analyst') THEN CREATE ROLE netflix_data_analyst; END IF; END $$;",
            "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'netflix_data_scientist') THEN CREATE ROLE netflix_data_scientist; END IF; END $$;",
            # Grant permissions to roles
            "GRANT SELECT ON ALL TABLES IN SCHEMA public TO netflix_data_analyst;",
            "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO netflix_data_analyst;",
            "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO netflix_data_scientist;",
            "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO netflix_data_scientist;",
            # Check and create users if they don't exist, then grant roles
            "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'netflix_user_analyst') THEN CREATE USER netflix_user_analyst WITH PASSWORD 'secure_password1'; END IF; END $$;",
            "GRANT netflix_data_analyst TO netflix_user_analyst;",
            "DO $$ BEGIN IF NOT EXISTS (SELECT FROM pg_user WHERE usename = 'netflix_user_scientist') THEN CREATE USER netflix_user_scientist WITH PASSWORD 'secure_password2'; END IF; END $$;",
            "GRANT netflix_data_scientist TO netflix_user_scientist;",
        ]

        for cmd in commands:
            logging.info(f"Executing command: {cmd}")
            self.data_api.administrative_query(cmd)
            logging.info("Command executed successfully.")


if __name__ == "__main__":
    data_api = DataAPI(db_config)

    db_permissions = DatabasePermissions(data_api)
    db_permissions.setup_permissions()
