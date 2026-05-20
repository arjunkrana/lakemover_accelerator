SQL_MAPPINGS = {
    "NVL(": "COALESCE(",
    "SYSDATE": "CURRENT_DATE",
    "VARCHAR2": "VARCHAR",
    "NUMBER": "NUMERIC"
}


def convert_sql(statement):

    converted_sql = statement

    for old_syntax, new_syntax in SQL_MAPPINGS.items():

        converted_sql = converted_sql.replace(
            old_syntax,
            new_syntax
        )

    return converted_sql