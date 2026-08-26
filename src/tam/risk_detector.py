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


def detect_account_risks(
    account: dict,
    tickets: list[dict],
) -> list[dict]:
    """
    Detect deterministic churn and escalation signals
    from account metadata and recent ticket history.
    """

    risks = []

    # ---------------------------------------------------------
    # 1. Account-level escalation notes
    # ---------------------------------------------------------

    for note in account.get("escalation_notes", []):
        note_lower = note.lower()

        if any(
            keyword in note_lower
            for keyword in RISK_KEYWORDS["churn"]
        ):
            risks.append(
                {
                    "type": "churn",
                    "source": "account",
                    "evidence": note,
                }
            )

        elif any(
            keyword in note_lower
            for keyword in RISK_KEYWORDS["escalation"]
        ):
            risks.append(
                {
                    "type": "escalation",
                    "source": "account",
                    "evidence": note,
                }
            )

    # ---------------------------------------------------------
    # 2. Structured P1 escalation signal
    # ---------------------------------------------------------

    p1_count = account.get("p1_tickets_last_30d", 0)

    if p1_count >= 2:
        risks.append(
            {
                "type": "escalation",
                "source": "account",
                "evidence": (
                    f"{p1_count} P1 tickets in the last 30 days"
                ),
            }
        )

    # ---------------------------------------------------------
    # 3. Ticket-level churn / escalation signals
    # ---------------------------------------------------------

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
                risks.append(
                    {
                        "type": risk_type,
                        "source": "ticket",
                        "ticket_id": ticket["ticket_id"],
                        "evidence": body,
                        "matched_keywords": matched,
                    }
                )

    return risks