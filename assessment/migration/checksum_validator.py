import pandas as pd
import hashlib


def generate_dataframe_checksum(df):

    checksum_string = ""

    for _, row in df.iterrows():

        checksum_string += "".join(
            row.astype(str)
        )

    checksum = hashlib.md5(
        checksum_string.encode()
    ).hexdigest()

    return checksum


def validate_checksums(
        source_engine,
        lakebase_engine,
        table_name):

    try:

        source_query = f'''
        SELECT *
        FROM "{table_name}"
        ORDER BY 1
        '''

        sanitized_table_name = (
            table_name
            .replace("-", "_")
            .replace(" ", "_")
            .lower()
        )

        target_query = f"""
        SELECT *
        FROM {sanitized_table_name}
        ORDER BY 1
        """

        source_df = pd.read_sql(
            source_query,
            source_engine
        )

        target_df = pd.read_sql(
            target_query,
            lakebase_engine
        )

        source_checksum = generate_dataframe_checksum(
            source_df
        )

        target_checksum = generate_dataframe_checksum(
            target_df
        )

        return {
            "table": sanitized_table_name,
            "source_checksum": source_checksum,
            "target_checksum": target_checksum,
            "status": "PASS"
            if source_checksum == target_checksum
            else "FAIL"
        }

    except Exception as error:

        return {
            "table": table_name,
            "status": "FAILED",
            "error": str(error)
        }