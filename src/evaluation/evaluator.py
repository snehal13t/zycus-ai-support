from typing import Any


def _sentence_count(text: str) -> int:
    return sum(
        1
        for char in text
        if char in ".!?"
    )


def evaluate_triage_result(
    result: Any,
    criteria: dict,
) -> dict:
    """
    Evaluate a Task 1 triage result using deterministic criteria.
    """

    checks = []

    if "issue_category" in criteria:
        checks.append(
            result.issue_category
            == criteria["issue_category"]
        )

    if "urgency" in criteria:
        expected = criteria["urgency"]

        if isinstance(expected, list):
            checks.append(result.urgency in expected)
        else:
            checks.append(result.urgency == expected)

    if "urgency_not" in criteria:
        checks.append(
            result.urgency != criteria["urgency_not"]
        )

    if "product_area_contains" in criteria:
        checks.append(
            criteria["product_area_contains"].lower()
            in result.product_area.lower()
        )

    if "known_issue" in criteria:
        checks.append(
            result.known_issue
            == criteria["known_issue"]
        )

    if "kb_section_contains" in criteria:
        section = ""

        if result.kb_reference:
            section = result.kb_reference.section

        checks.append(
            criteria["kb_section_contains"].lower()
            in section.lower()
        )

    if "first_response_nonempty" in criteria:
        checks.append(
            bool(result.first_response.strip())
        )

    score = (
        sum(checks) / len(checks)
        if checks
        else 0.0
    )

    return {
        "quality_score": round(score, 3),
        "status": "PASS" if score == 1.0 else "FAIL",
        "checks_passed": sum(checks),
        "checks_total": len(checks),
    }


def evaluate_account_brief(
    brief: Any,
    criteria: dict,
) -> dict:
    """
    Evaluate a Task 2 account brief using deterministic criteria.
    """

    checks = []

    if "summary_sentence_range" in criteria:
        minimum, maximum = criteria[
            "summary_sentence_range"
        ]

        count = _sentence_count(
            brief.executive_summary
        )

        checks.append(
            minimum <= count <= maximum
        )

    if "risk_type" in criteria:
        checks.append(
            any(
                risk.risk_type == criteria["risk_type"]
                for risk in brief.open_risks
            )
        )

    if "risk_count_min" in criteria:
        checks.append(
            len(brief.open_risks)
            >= criteria["risk_count_min"]
        )

    if "talking_points_min" in criteria:
        checks.append(
            len(brief.talking_points)
            >= criteria["talking_points_min"]
        )

    if "no_crash" in criteria:
        checks.append(True)

    score = (
        sum(checks) / len(checks)
        if checks
        else 0.0
    )

    return {
        "quality_score": round(score, 3),
        "status": "PASS" if score == 1.0 else "FAIL",
        "checks_passed": sum(checks),
        "checks_total": len(checks),
    }