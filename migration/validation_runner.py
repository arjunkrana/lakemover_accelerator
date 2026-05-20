import pandas as pd


def validate_row_counts(
    source_engine,
    lakebase_engine,
    table_name
):

    sanitized_table_name = (
        table_name
        .replace("-", "_")
        .replace(" ", "_")
        .lower()
    )

    try:

        # ==================================
        # SOURCE COUNT
        # ==================================

        source_query = f'''
        SELECT COUNT(*) AS total_count
        FROM "{table_name}"
        '''

        source_df = pd.read_sql(
            source_query,
            source_engine
        )

        # ==================================
        # TARGET COUNT
        # ==================================

        target_query = f'''
        SELECT COUNT(*) AS total_count
        FROM "{sanitized_table_name}"
        '''

        target_df = pd.read_sql(
            target_query,
            lakebase_engine
        )

        # ==================================
        # SAFE EXTRACTION
        # ==================================

        source_count = int(
            source_df["total_count"].iloc[0]
        )

        target_count = int(
            target_df["total_count"].iloc[0]
        )

        return {
            "table": sanitized_table_name,
            "source_count": source_count,
            "target_count": target_count,
            "status":
            "PASS"
            if source_count == target_count
            else "FAIL"
        }

    except Exception as error:

        return {
            "table": sanitized_table_name,
            "status": "FAILED",
            "error": str(error)
        }