import pandas as pd
from sqlalchemy import text


def sanitize_table_name(table_name):

    sanitized = (
        table_name
        .replace("-", "_")
        .replace(" ", "_")
        .lower()
    )

    return sanitized


def get_source_tables(source_engine):

    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    """

    return pd.read_sql(query, source_engine)


def get_table_columns(source_engine, table_name):

    query = f"""
    SELECT
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_name = '{table_name}'
    ORDER BY ordinal_position
    """

    return pd.read_sql(query, source_engine)


def map_datatypes(postgres_type):

    mapping = {
        "integer": "INTEGER",
        "bigint": "BIGINT",
        "character varying": "VARCHAR(255)",
        "text": "TEXT",
        "boolean": "BOOLEAN",
        "timestamp without time zone": "TIMESTAMP"
    }

    return mapping.get(postgres_type, "TEXT")


def generate_create_statement(
        table_name,
        columns_df):

    sanitized_table_name = sanitize_table_name(
        table_name
    )

    column_definitions = []

    for _, row in columns_df.iterrows():

        column_name = row["column_name"]
        datatype = map_datatypes(row["data_type"])

        column_definitions.append(
            f"{column_name} {datatype}"
        )

    column_sql = ",\n".join(column_definitions)

    create_sql = f"""
    CREATE TABLE IF NOT EXISTS {sanitized_table_name} (
        {column_sql}
    );
    """

    return create_sql


def migrate_schema(
        source_engine,
        lakebase_engine):

    tables = get_source_tables(source_engine)

    for _, table in tables.iterrows():

        table_name = table["table_name"]

        try:

            columns_df = get_table_columns(
                source_engine,
                table_name
            )

            create_sql = generate_create_statement(
                table_name,
                columns_df
            )

            print(f"Creating table: {table_name}")

            with lakebase_engine.begin() as conn:

                conn.execute(text(create_sql))

            print(f"Table created: {table_name}")

        except Exception as error:

            print(
                f"Schema migration failed for "
                f"{table_name}: {error}"
            )