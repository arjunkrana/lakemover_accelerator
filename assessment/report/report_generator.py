from jinja2 import Environment, FileSystemLoader
import json

def generate_report(findings, readiness_score):

    env = Environment(
        loader=FileSystemLoader("assessment/report")
    )

    template = env.get_template("template.html")

    html_content = template.render(
        findings=findings,
        readiness_score=readiness_score
    )

    with open(
        "assessment/outputs/assessment_report.html",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html_content)

    with open(
        "assessment/outputs/findings.json",
        "w"
    ) as f:

        json.dump(findings, f, indent=4)