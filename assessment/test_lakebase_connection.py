from connectors.lakebase_connector import (
    get_lakebase_connection
)

engine = get_lakebase_connection()

connection = engine.connect()

print("Lakebase Connected Successfully")

connection.close()