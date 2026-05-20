UNSUPPORTED_PATTERNS = [
    "NVL(",
    "DECODE(",
    "CONNECT BY",
    "TEMP TABLE",
    "CREATE PROCEDURE",
    "CREATE TRIGGER"
]


def validate_sql(parsed_statements):

    findings = []

    for stmt in parsed_statements:

        statement = stmt["statement"]

        for pattern in UNSUPPORTED_PATTERNS:

            if pattern in statement.upper():

                findings.append({
                    "severity": "WARNING",
                    "issue":
                    f"Unsupported SQL syntax: {pattern}",
                    "statement": statement,
                    "recommendation":
                    "Convert syntax before migration"
                })

    return findings