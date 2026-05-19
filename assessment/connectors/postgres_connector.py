from sqlalchemy import create_engine
import yaml

def get_connection():

    with open("config/db_config.yaml") as f:
        config = yaml.safe_load(f)

    connection_string = (
        f"postgresql://"
        f"{config['source_username']}:"
        f"{config['source_password']}@"
        f"{config['source_host']}:"
        f"{config['source_port']}/"
        f"{config['source_database']}"
    )

    engine = create_engine(connection_string)

    return engine