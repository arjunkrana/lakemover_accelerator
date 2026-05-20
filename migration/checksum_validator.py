import hashlib
import pandas as pd


def generate_checksum(df):

    checksum_string = ""

    for _, row in df.iterrows():

        row_string = "|".join(
            row.astype(str)
        )

        checksum_string += row_string

    return hashlib.md5(
        checksum_string.encode()
    ).hexdigest()


def validate_checksums(
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
        # SOURCE QUERY
        # ==================================

        source_query = f'''
        SELECT *
        FROM "{table_name}"
        ORDER BY 1
        '''

        source_df = pd.read_sql(
            source_query,
            source_engine
        )

        # ==================================
        # TARGET QUERY
        # ==================================

        target_query = f'''
        SELECT *
        FROM "{sanitized_table_name}"
        ORDER BY 1
        '''

        target_df = pd.read_sql(
            target_query,
            lakebase_engine
        )

        # ==================================
        # CHECKSUM GENERATION
        # ==================================

        source_checksum = generate_checksum(
            source_df
        )

        target_checksum = generate_checksum(
            target_df
        )

        return {
            "table": sanitized_table_name,
            "source_checksum":
            source_checksum,
            "target_checksum":
            target_checksum,
            "status":
            "PASS"
            if source_checksum
            == target_checksum
            else "FAIL"
        }

    except Exception as error:

        return {
            "table": sanitized_table_name,
            "status": "FAILED",
            "error": str(error)
        }