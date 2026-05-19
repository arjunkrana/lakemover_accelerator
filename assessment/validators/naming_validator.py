import re
import yaml

def validate_table_names(tables_df):

    with open("config/rules.yaml") as f:
        rules = yaml.safe_load(f)

    pattern = rules["naming_pattern"]

    findings = []

    for _, row in tables_df.iterrows():

        table_name = row["table_name"]

        if not re.match(pattern, table_name):

            findings.append({
                "severity": "BLOCKER",
                "issue": "Invalid table name",
                "table": table_name,
                "recommendation":
                "Rename table using only A-Z a-z 0-9 _"
            })

    return findings