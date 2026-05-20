import pandas as pd

UNSUPPORTED_TYPES = [
    "tsvector",
    "xml",
    "cidr"
]

def validate_datatypes(engine):

    query = """
    SELECT
        table_name,
        column_name,
        data_type
    FROM information_schema.columns;
    """

    df = pd.read_sql(query, engine)

    findings = []

    for _, row in df.iterrows():

        if row["data_type"] in UNSUPPORTED_TYPES:

            findings.append({
                "severity": "BLOCKER",
                "issue": "Unsupported datatype",
                "table": row["table_name"],
                "column": row["column_name"],
                "datatype": row["data_type"],
                "recommendation":
                "Convert datatype before migration"
            })

    return findings