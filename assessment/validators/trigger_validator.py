import pandas as pd

def validate_triggers(engine):

    query = """
    SELECT
        trigger_name,
        event_object_table
    FROM information_schema.triggers
    WHERE trigger_schema = 'public';
    """

    df = pd.read_sql(query, engine)

    findings = []

    for _, row in df.iterrows():

        findings.append({
            "severity": "WARNING",
            "issue": "Trigger detected",
            "table": row["event_object_table"],
            "trigger": row["trigger_name"],
            "recommendation":
            "Rewrite trigger logic externally"
        })

    return findings