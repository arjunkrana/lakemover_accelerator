import pandas as pd

from connectors.lakebase_connector import (
    get_lakebase_connection
)

engine = get_lakebase_connection()

query = """
SELECT *
FROM customers_test;
"""

df = pd.read_sql(query, engine)

print(df)