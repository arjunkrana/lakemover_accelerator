import pandas as pd

def validate_null_bytes(engine, tables_df):

    findings = []

    for _, row in tables_df.iterrows():

        schema_name = row["table_schema"]
        table_name = row["table_name"]

        try:

            # Get text columns only
            column_query = f"""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = '{schema_name}'
            AND table_name = '{table_name}'
            AND data_type IN ('text', 'character varying');
            """

            columns_df = pd.read_sql(column_query, engine)

            for column in columns_df["column_name"]:

                validation_query = f"""
                SELECT COUNT(*) AS null_count
                FROM "{schema_name}"."{table_name}"
                WHERE "{column}" LIKE '%' || chr(0) || '%';
                """

                result_df = pd.read_sql(validation_query, engine)

                null_count = result_df.iloc[0]["null_count"]

                if null_count > 0:

                    findings.append({
                        "severity": "BLOCKER",
                        "issue": "Null byte detected",
                        "schema": schema_name,
                        "table": table_name,
                        "column": column,
                        "affected_rows": int(null_count),
                        "recommendation":
                        "Remove null byte characters before migration"
                    })

        except Exception as e:

            findings.append({
                "severity": "WARNING",
                "issue": "Null byte validation failed",
                "schema": schema_name,
                "table": table_name,
                "error": str(e)
            })

    return findings