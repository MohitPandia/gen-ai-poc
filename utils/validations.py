import re

DISALLOWED_SQL_COMMANDS = ["DELETE", "DROP", "TRUNCATE", "ALTER", "UPDATE"]

def validate_sql_query(query):
    for command in DISALLOWED_SQL_COMMANDS:
        if re.search(rf'\b{command}\b', query, re.IGNORECASE):
            return False
    return True
