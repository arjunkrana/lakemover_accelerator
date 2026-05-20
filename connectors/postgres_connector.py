import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def get_connection():

    host = os.getenv("SOURCE_HOST")
    port = os.getenv("SOURCE_PORT")
    database = os.getenv("SOURCE_DATABASE")
    username = os.getenv("SOURCE_USERNAME")
    password = os.getenv("SOURCE_PASSWORD")

    connection_string = (
        f"postgresql://{username}:{password}"
        f"@{host}:{port}/{database}"
    )

    engine = create_engine(
        connection_string
    )

    return engine