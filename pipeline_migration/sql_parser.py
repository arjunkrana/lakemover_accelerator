import os


def get_sql_files(folder_path):

    sql_files = []

    for root, _, files in os.walk(folder_path):

        for file in files:

            if file.endswith(".sql"):

                full_path = os.path.join(
                    root,
                    file
                )

                sql_files.append(full_path)

    return sql_files


def parse_sql_script(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        sql_content = file.read()

    statements = [
        stmt.strip()
        for stmt in sql_content.split(";")
        if stmt.strip()
    ]

    parsed_output = []

    for statement in statements:

        analysis = {
            "file_path": file_path,
            "statement": statement,
            "has_join": False,
            "has_temp_table": False,
            "has_cte": False,
            "has_insert": False,
            "has_procedure": False
        }

        upper_stmt = statement.upper()

        if " JOIN " in upper_stmt:
            analysis["has_join"] = True

        if "TEMP TABLE" in upper_stmt:
            analysis["has_temp_table"] = True

        if upper_stmt.startswith("WITH"):
            analysis["has_cte"] = True

        if upper_stmt.startswith("INSERT"):
            analysis["has_insert"] = True

        if "PROCEDURE" in upper_stmt:
            analysis["has_procedure"] = True

        parsed_output.append(analysis)

    return parsed_output