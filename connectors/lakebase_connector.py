import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def get_lakebase_connection():

    host = os.getenv("LAKEBASE_HOST")
    port = os.getenv("LAKEBASE_PORT")
    database = os.getenv("LAKEBASE_DATABASE")
    username = os.getenv("LAKEBASE_USERNAME")
    password = os.getenv("LAKEBASE_PASSWORD")
    sslmode = os.getenv("LAKEBASE_SSLMODE")

    connection_string = (
        f"postgresql://{username}:{password}"
        f"@{host}:{port}/{database}"
        f"?sslmode={sslmode}"
    )

    engine = create_engine(
        connection_string
    )

    return engine