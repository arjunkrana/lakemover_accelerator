import json
import numpy as np
from datetime import datetime


def convert_numpy_types(obj):

    if isinstance(obj, np.integer):
        return int(obj)

    elif isinstance(obj, np.floating):
        return float(obj)

    elif isinstance(obj, np.ndarray):
        return obj.tolist()

    return str(obj)


def log_audit_event(
    event_type,
    status,
    details
):

    audit_record = {
        "timestamp": str(datetime.now()),
        "event_type": event_type,
        "status": status,
        "details": details
    }

    with open(
        "audit/audit_log.json",
        "a"
    ) as file:

        file.write(
            json.dumps(
                audit_record,
                default=convert_numpy_types
            )
        )

        file.write("\n")