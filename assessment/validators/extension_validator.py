import pandas as pd
import yaml

def validate_extensions(engine):

    with open("config/rules.yaml") as f:
        rules = yaml.safe_load(f)

    unsupported = rules["unsupported_extensions"]

    query = """
    SELECT extname
    FROM pg_extension;
    """

    df = pd.read_sql(query, engine)

    findings = []

    for ext in df["extname"]:

        if ext in unsupported:

            findings.append({
                "severity": "BLOCKER",
                "issue": "Unsupported extension",
                "extension": ext,
                "recommendation":
                "Replace unsupported extension"
            })

    return findings