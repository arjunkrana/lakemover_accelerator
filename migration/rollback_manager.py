from sqlalchemy import text


def rollback_table(
    lakebase_engine,
    table_name
):

    sanitized_table_name = (
        table_name
        .replace("-", "_")
        .replace(" ", "_")
        .lower()
    )

    query = f'''
    DROP TABLE IF EXISTS "{sanitized_table_name}"
    '''

    with lakebase_engine.begin() as conn:

        conn.execute(
            text(query)
        )

    print(
        f"Rollback completed: "
        f"{sanitized_table_name}"
    )