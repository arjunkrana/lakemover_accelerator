from sqlalchemy import create_engine
import yaml

def get_lakebase_connection():

    with open("config/db_config.yaml") as f:
        config = yaml.safe_load(f)

    connection_string = (
        f"postgresql://"
        f"{config['lakebase_username']}:"
        f"{config['lakebase_password']}@"
        f"{config['lakebase_host']}:"
        f"{config['lakebase_port']}/"
        f"{config['lakebase_database']}?"
        f"sslmode={config['lakebase_sslmode']}"
    )

    engine = create_engine(connection_string)

    return engine