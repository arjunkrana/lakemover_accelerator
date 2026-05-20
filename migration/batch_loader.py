import pandas as pd
from sqlalchemy import text


def migrate_in_batches(
    source_engine,
    lakebase_engine,
    table_name,
    batch_size=100000
):

    sanitized_table_name = (
        table_name
        .replace("-", "_")
        .replace(" ", "_")
        .lower()
    )

    # =====================================
    # CLEAN TARGET TABLE BEFORE LOAD
    # =====================================

    with lakebase_engine.begin() as conn:

        conn.execute(
            text(
                f'''
                TRUNCATE TABLE
                "{sanitized_table_name}"
                '''
            )
        )

    print(
        f"Target table truncated: "
        f"{sanitized_table_name}"
    )

    # =====================================
    # BATCH MIGRATION
    # =====================================

    offset = 0

    while True:

        query = f"""
        SELECT *
        FROM "{table_name}"
        LIMIT {batch_size}
        OFFSET {offset};
        """

        df = pd.read_sql(
            query,
            source_engine
        )

        if df.empty:
            break

        df.to_sql(
            sanitized_table_name,
            lakebase_engine,
            if_exists="append",
            index=False
        )

        print(
            f"Migrated batch "
            f"starting at offset {offset}"
        )

        offset += batch_size