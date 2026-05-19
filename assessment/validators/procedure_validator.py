import pandas as pd

def validate_procedures(engine):

    query = """
    SELECT
        r.routine_name
    FROM information_schema.routines r
    WHERE r.routine_schema = 'public'
    AND r.routine_name NOT IN (

        SELECT p.proname
        FROM pg_proc p
        JOIN pg_depend d
            ON d.objid = p.oid
        JOIN pg_extension e
            ON e.oid = d.refobjid

    );
    """

    df = pd.read_sql(query, engine)

    findings = []

    for _, row in df.iterrows():

        findings.append({
            "severity": "WARNING",
            "issue": "Stored procedure detected",
            "procedure": row["routine_name"],
            "recommendation":
            "Rewrite procedure logic externally"
        })

    return findings