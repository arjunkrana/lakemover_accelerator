import json


def generate_pipeline_report(
    parsed_statements,
    validation_findings,
    dependencies
):

    report = {
        "total_statements":
        len(parsed_statements),

        "validation_findings":
        validation_findings,

        "dependencies":
        dependencies
    }

    with open(
        "assessment/outputs/pipeline_report.json",
        "w"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    print(
        "Pipeline Migration Report Generated"
    )