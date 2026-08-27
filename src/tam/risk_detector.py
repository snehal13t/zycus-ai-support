RISK_KEYWORDS = {
    "churn": [
        "cancel",
        "cancellation",
        "churn",
        "competitor",
        "competing vendor",
        "switching",
        "replace",
        "replacement",
        "renewal concern",
    ],
    "escalation": [
        "escalation",
        "escalated",
        "urgent",
        "frustrated",
        "frustration",
        "unhappy",
        "negative sentiment",
        "executive escalation",
    ],
}


def _extract_quote(
    subject: str,
    body: str,
    matched_keywords: list[str],
) -> str:
    """Extract a concise direct quote containing a risk signal."""

    lines = [
        line.strip()
        for line in body.splitlines()
        if line.strip()
    ]

    for keyword in matched_keywords:
        for line in lines:
            if keyword.lower() in line.lower():
                return line

    if lines:
        return lines[0]

    return subject.strip()


def detect_account_risks(
    account: dict,
    tickets: list[dict],
) -> list[dict]:
    """Detect deterministic churn and escalation signals."""

    risks = []

    for note in account.get("escalation_notes", []):
        note_lower = note.lower()

        if any(
            keyword in note_lower
            for keyword in RISK_KEYWORDS["churn"]
        ):
            risks.append({
                "type": "churn",
                "source": "account",
                "evidence": note,
            })

        elif any(
            keyword in note_lower
            for keyword in RISK_KEYWORDS["escalation"]
        ):
            risks.append({
                "type": "escalation",
                "source": "account",
                "evidence": note,
            })

    p1_count = account.get("p1_tickets_last_30d", 0)

    if p1_count >= 2:
        risks.append({
            "type": "escalation",
            "source": "account",
            "evidence": (
                f"{p1_count} P1 tickets in the last 30 days"
            ),
        })

    for ticket in tickets:
        subject = ticket.get("subject", "")
        body = ticket.get("body", "")

        text = f"{subject} {body}".lower()

        for risk_type in ("churn", "escalation"):
            matched = [
                keyword
                for keyword in RISK_KEYWORDS[risk_type]
                if keyword in text
            ]

            if matched:
                quote = _extract_quote(
                    subject,
                    body,
                    matched,
                )

                risks.append({
                    "type": risk_type,
                    "source": "ticket",
                    "ticket_id": ticket["ticket_id"],
                    "evidence": (
                        f"Matched risk keywords: "
                        f"{', '.join(matched)}"
                    ),
                    "quote": quote,
                    "matched_keywords": matched,
                })

    return risks
