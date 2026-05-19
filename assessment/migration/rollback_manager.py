from sqlalchemy import text


def rollback_table(lakebase_engine, table_name):

    query = f"DROP TABLE IF EXISTS {table_name}"

    with lakebase_engine.begin() as conn:
        conn.execute(text(query))

    print(f"Rollback completed: {table_name}")