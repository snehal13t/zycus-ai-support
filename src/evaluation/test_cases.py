TASK1_CASES = [
    {
        "id": "T1-01",
        "name": "Feature request with incorrect historical label",
        "ticket_id": "TKT-10000",
        "criteria": {
            "issue_category": "Feature Request",
            "urgency": "P3",
            "product_area_contains": "Data Ingestion",
        },
    },
    {
        "id": "T1-02",
        "name": "SSO new-user authentication issue",
        "ticket_id": None,
        "subject": "New users cannot authenticate via SSO",
        "body": (
            "Existing users can log in but new joiners cannot authenticate. "
            "They receive an authentication error."
        ),
        "criteria": {
            "product_area_contains": "SSO",
            "urgency_not": "P1",
            "known_issue": True,
            "kb_section_contains": "New Users Cannot Authenticate via SSO",
        },
    },
    {
        "id": "T1-03",
        "name": "Production performance issue",
        "ticket_id": None,
        "subject": "Production pipeline is extremely slow",
        "body": (
            "Our production pipeline is processing data much slower than usual. "
            "The issue has affected multiple users."
        ),
        "criteria": {
            "issue_category": "Performance",
            "urgency": ["P1", "P2"],
        },
    },
    {
        "id": "T1-04",
        "name": "Billing question",
        "ticket_id": None,
        "subject": "Question about invoice and seat charges",
        "body": (
            "We need clarification on our invoice and how active seats "
            "are counted for billing."
        ),
        "criteria": {
            "issue_category": "Billing",
            "urgency": ["P3", "P4"],
            "kb_type": "billing",
        },
    },
    {
        "id": "T1-05",
        "name": "Ambiguous adversarial ticket",
        "ticket_id": None,
        "subject": "Everything is broken",
        "body": (
            "Things aren't working properly. Please help. "
            "We need someone to look into this."
        ),
        "criteria": {
            "urgency_not": "P1",
            "first_response_nonempty": True,
        },
    },
]


TASK2_CASES = [
    {
        "id": "T2-01",
        "name": "At-risk account with escalation signals",
        "account_id": "ACC-7397",
        "criteria": {
            "summary_sentence_range": (3, 5),
            "risk_type": "escalation",
            "risk_count_min": 1,
            "talking_points_min": 2,
        },
    },
    {
        "id": "T2-02",
        "name": "At-risk account with sparse ticket history",
        "account_id": "ACC-3336",
        "criteria": {
            "summary_sentence_range": (3, 5),
            "talking_points_min": 1,
        },
    },
    {
        "id": "T2-03",
        "name": "Healthy account with limited signals",
        "account_id": "ACC-9634",
        "criteria": {
            "summary_sentence_range": (3, 5),
            "talking_points_min": 1,
        },
    },
    {
        "id": "T2-04",
        "name": "New customer account",
        "account_id": "ACC-5748",
        "criteria": {
            "summary_sentence_range": (3, 5),
            "talking_points_min": 1,
        },
    },
    {
        "id": "T2-05",
        "name": "Incomplete account data — adversarial",
        "account_id": "ACC-3336",
        "criteria": {
            "summary_sentence_range": (3, 5),
            "no_crash": True,
            "talking_points_min": 1,
        },
    },
]