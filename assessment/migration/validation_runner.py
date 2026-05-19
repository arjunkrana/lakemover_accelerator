import pandas as pd


def sanitize_table_name(table_name):

    sanitized = (
        table_name
        .replace("-", "_")
        .replace(" ", "_")
        .lower()
    )

    return sanitized


def validate_row_counts(
        source_engine,
        lakebase_engine,
        table_name):

    try:

        source_query = f'''
        SELECT COUNT(*) as count
        FROM "{table_name}"
        '''

        sanitized_table_name = sanitize_table_name(
            table_name
        )

        target_query = f"""
        SELECT COUNT(*) as count
        FROM {sanitized_table_name}
        """

        source_count = pd.read_sql(
            source_query,
            source_engine
        )["count"][0]

        target_count = pd.read_sql(
            target_query,
            lakebase_engine
        )["count"][0]

        validation = {
            "table": sanitized_table_name,
            "source_count": source_count,
            "target_count": target_count,
            "status": "PASS"
            if source_count == target_count
            else "FAIL"
        }

        return validation

    except Exception as error:

        return {
            "table": table_name,
            "status": "FAILED",
            "error": str(error)
        }