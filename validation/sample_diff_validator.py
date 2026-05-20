import pandas as pd


def validate_sample_diff(
    source_engine,
    lakebase_engine,
    table_name
):

    try:

        sanitized_table_name = (
            table_name
            .replace("-", "_")
            .replace(" ", "_")
            .lower()
        )

        # ==================================
        # SOURCE SAMPLE
        # ==================================

        source_query = f'''
        SELECT *
        FROM "{table_name}"
        ORDER BY 1
        LIMIT 100
        '''

        source_df = pd.read_sql(
            source_query,
            source_engine
        )

        # ==================================
        # TARGET SAMPLE
        # ==================================

        target_query = f'''
        SELECT *
        FROM "{sanitized_table_name}"
        ORDER BY 1
        LIMIT 100
        '''

        target_df = pd.read_sql(
            target_query,
            lakebase_engine
        )

        # ==================================
        # STRING NORMALIZATION
        # ==================================

        source_rows = source_df.astype(
            str
        ).apply(
            lambda x: "|".join(x),
            axis=1
        )

        target_rows = set(
            target_df.astype(str).apply(
                lambda x: "|".join(x),
                axis=1
            )
        )

        mismatches = 0

        for row in source_rows:

            if row not in target_rows:

                mismatches += 1

        return {
            "table": sanitized_table_name,
            "mismatches": mismatches,
            "status":
            "PASS"
            if mismatches == 0
            else "FAIL"
        }

    except Exception as error:

        return {
            "table": sanitized_table_name,
            "status": "FAILED",
            "error": str(error)
        }