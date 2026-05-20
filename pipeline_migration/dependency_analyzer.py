import re


def analyze_dependencies(parsed_statements):

    dependencies = []

    for stmt in parsed_statements:

        statement = stmt["statement"]

        tables = re.findall(
            r'FROM\s+([a-zA-Z0-9_]+)',
            statement,
            re.IGNORECASE
        )

        joins = re.findall(
            r'JOIN\s+([a-zA-Z0-9_]+)',
            statement,
            re.IGNORECASE
        )

        dependencies.append({
            "statement": statement,
            "source_tables": tables,
            "joined_tables": joins
        })

    return dependencies