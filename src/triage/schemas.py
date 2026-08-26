from dataclasses import dataclass
from typing import Optional


@dataclass
class KBReference:
    source: str
    section: str
    relevance_score: float


@dataclass
class TriageResult:
    product_area: str
    issue_category: str
    urgency: str
    urgency_reason: str
    reasoning: str
    known_issue: bool
    kb_reference: Optional[KBReference]
    responder_team: str
    first_response: str