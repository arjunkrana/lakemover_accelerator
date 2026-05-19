import pandas as pd
import yaml

def validate_table_size(engine):

    with open("config/rules.yaml") as f:
        rules = yaml.safe_load(f)

    threshold = rules["table_size_threshold_gb"]

    query = """
    SELECT
        relname AS table_name,
        pg_total_relation_size(relid)
/1024/1024/1024 AS size_gb
    FROM pg_catalog.pg_statio_user_tables
    ORDER BY size_gb DESC;
    """

    df = pd.read_sql(query, engine)

    findings = []

    for _, row in df.iterrows():

        if row["size_gb"] > threshold:

            findings.append({
                "severity": "WARNING",
                "issue": "Large table detected",
                "table": row["table_name"],
                "size_gb": float(row["size_gb"]),
                "recommendation":
                "Consider partition migration strategy"
            })

    return findings