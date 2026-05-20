def detect_drift(
    source_count,
    target_count
):

    if source_count != target_count:

        return {
            "status": "DRIFT_DETECTED",
            "difference":
            source_count - target_count
        }

    return {
        "status": "NO_DRIFT"
    }