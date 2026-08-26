import json
from pathlib import Path

from src.evaluation.evaluator import (
    evaluate_account_brief,
    evaluate_triage_result,
)
from src.evaluation.test_cases import (
    TASK1_CASES,
    TASK2_CASES,
)


TASK1_FIXTURES = Path(
    "evaluation/fixtures/task1_outputs.json"
)

TASK2_FIXTURES = Path(
    "evaluation/fixtures/task2_outputs.json"
)


def load_json(path: Path) -> dict:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def make_triage_result(data: dict):
    """
    Convert fixture JSON into the same attribute-based
    structure expected by the evaluator.
    """

    class KBReference:
        def __init__(self, value):
            self.source = value.get("source")
            self.section = value.get("section")
            self.relevance_score = value.get(
                "relevance_score"
            )

    class TriageResult:
        pass

    result = TriageResult()

    result.product_area = data["product_area"]
    result.issue_category = data["issue_category"]
    result.urgency = data["urgency"]
    result.known_issue = data["known_issue"]

    kb_reference = data.get("kb_reference")

    result.kb_reference = (
        KBReference(kb_reference)
        if kb_reference
        else None
    )

    result.first_response = data[
        "first_response"
    ]

    return result


def make_account_brief(data: dict):
    """
    Convert fixture JSON into the same attribute-based
    structure expected by the evaluator.
    """

    class RiskFlag:
        def __init__(self, value):
            self.risk_type = value["risk_type"]
            self.source = value["source"]
            self.evidence = value["evidence"]
            self.ticket_id = value.get("ticket_id")
            self.quote = value.get("quote")

    class AccountBrief:
        pass

    brief = AccountBrief()

    brief.executive_summary = data[
        "executive_summary"
    ]

    brief.open_risks = [
        RiskFlag(risk)
        for risk in data["open_risks"]
    ]

    brief.talking_points = data[
        "talking_points"
    ]

    return brief


task1_outputs = load_json(
    TASK1_FIXTURES
)

task2_outputs = load_json(
    TASK2_FIXTURES
)


results = {
    "task1": [],
    "task2": [],
}


# ============================================================
# TASK 1
# ============================================================

for case in TASK1_CASES:

    output = task1_outputs[case["id"]]

    result = make_triage_result(output)

    evaluation = evaluate_triage_result(
        result,
        case["criteria"],
    )

    results["task1"].append(
        {
            "test_id": case["id"],
            "name": case["name"],
            "status": evaluation["status"],
            "quality_score": evaluation[
                "quality_score"
            ],
            "checks_passed": evaluation[
                "checks_passed"
            ],
            "checks_total": evaluation[
                "checks_total"
            ],
        }
    )


# ============================================================
# TASK 2
# ============================================================

for case in TASK2_CASES:

    output = task2_outputs[case["id"]]

    brief = make_account_brief(output)

    evaluation = evaluate_account_brief(
        brief,
        case["criteria"],
    )

    results["task2"].append(
        {
            "test_id": case["id"],
            "name": case["name"],
            "status": evaluation["status"],
            "quality_score": evaluation[
                "quality_score"
            ],
            "checks_passed": evaluation[
                "checks_passed"
            ],
            "checks_total": evaluation[
                "checks_total"
            ],
        }
    )


# ============================================================
# SUMMARY
# ============================================================

for task_name in ("task1", "task2"):

    task_results = results[task_name]

    scores = [
        result["quality_score"]
        for result in task_results
    ]

    results[task_name + "_summary"] = {
        "tests": len(task_results),
        "passed": sum(
            result["status"] == "PASS"
            for result in task_results
        ),
        "average_quality_score": round(
            sum(scores) / len(scores),
            3,
        ),
    }


Path("eval_report.json").write_text(
    json.dumps(
        results,
        indent=2,
    ),
    encoding="utf-8",
)


print("\n" + "=" * 70)
print("OFFLINE EVALUATION REPORT")
print("=" * 70)

for task_name in ("task1", "task2"):

    summary = results[
        task_name + "_summary"
    ]

    print(
        f"\n{task_name.upper()}: "
        f"{summary['passed']}/{summary['tests']} passed "
        f"| Average score: "
        f"{summary['average_quality_score']}"
    )

    for result in results[task_name]:
        print(
            f"  {result['test_id']}: "
            f"{result['status']} "
            f"({result['quality_score']})"
        )

print("\nReport written to eval_report.json")