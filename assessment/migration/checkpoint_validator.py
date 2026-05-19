import json
from datetime import datetime


def create_checkpoint(table_name, status):

    checkpoint = {
        "table": table_name,
        "status": status,
        "timestamp": str(datetime.now())
    }

    with open(
            f"assessment/outputs/migration_logs/{table_name}.json",
            "w") as file:

        json.dump(checkpoint, file, indent=4)