import pandas as pd


def sanitize_table_name(table_name):

    sanitized = (
        table_name
        .replace("-", "_")
        .replace(" ", "_")
        .lower()
    )

    return sanitized


def migrate_table_data(
        source_engine,
        lakebase_engine,
        table_name):

    try:

        print(f"Migrating table: {table_name}")

        query = f'SELECT * FROM "{table_name}"'

        df = pd.read_sql(
            query,
            source_engine
        )

        sanitized_table_name = sanitize_table_name(
            table_name
        )

        df.to_sql(
            sanitized_table_name,
            lakebase_engine,
            if_exists='append',
            index=False
        )

        print(
            f"Completed migration: "
            f"{sanitized_table_name}"
        )

    except Exception as error:

        print(
            f"Data migration failed for "
            f"{table_name}: {error}"
        )