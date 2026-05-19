def calculate_readiness_score(findings):

    score = 100

    for finding in findings:

        if finding["severity"] == "BLOCKER":
            score -= 20

        elif finding["severity"] == "WARNING":
            score -= 5

    if score < 0:
        score = 0

    return score