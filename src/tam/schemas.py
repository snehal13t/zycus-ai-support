from dataclasses import dataclass


@dataclass
class RiskFlag:
    risk_type: str
    source: str
    evidence: str
    ticket_id: str | None = None
    quote: str | None = None


@dataclass
class AccountBrief:
    executive_summary: str
    open_risks: list[RiskFlag]
    talking_points: list[str]
