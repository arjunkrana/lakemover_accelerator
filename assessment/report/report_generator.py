from jinja2 import Environment, FileSystemLoader
import json
import time


def generate_report(
    findings,
    readiness_score
):

    env = Environment(
        loader=FileSystemLoader(
            "assessment/report/templates"
        )
    )

    template = env.get_template(
        "template.html"
    )

    html_content = template.render(
        findings=findings,
        readiness_score=readiness_score
    )

    timestamp = int(time.time())

    output_file = (
        f"assessment/outputs/"
        f"assessment_report_{timestamp}.html"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(html_content)

    with open(
        "assessment/outputs/findings.json",
        "w"
    ) as file:

        json.dump(
            findings,
            file,
            indent=4
        )

    print(
        f"\nHTML Report Generated: "
        f"{output_file}"
    )