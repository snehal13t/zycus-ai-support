import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from src.tam.account_loader import AccountLoader
from src.tam.risk_detector import detect_account_risks
from src.tam.schemas import AccountBrief, RiskFlag


load_dotenv()

def validate_brief_output(data: dict) -> None:
    """Validate the LLM-generated account brief."""

    required_fields = {
        "executive_summary",
        "open_risks",
        "talking_points",
    }

    missing = required_fields - data.keys()

    if missing:
        raise ValueError(
            f"Missing required brief fields: {sorted(missing)}"
        )

    if not isinstance(data["executive_summary"], str):
        raise ValueError("executive_summary must be a string.")

    sentence_count = sum(
        1
        for char in data["executive_summary"]
        if char in ".!?"
    )

    if sentence_count < 3 or sentence_count > 5:
        raise ValueError(
            "Executive summary must contain 3–5 sentences."
        )

    if not isinstance(data["open_risks"], list):
        raise ValueError("open_risks must be a list.")

    if not isinstance(data["talking_points"], list):
        raise ValueError("talking_points must be a list.")

    for risk in data["open_risks"]:
        required_risk_fields = {
            "risk_type",
            "source",
            "evidence",
            "ticket_id",
            "quote",
        }

        missing_risk = required_risk_fields - risk.keys()

        if missing_risk:
            raise ValueError(
                f"Missing risk fields: {sorted(missing_risk)}"
            )

        if risk["source"] == "ticket":
            if not risk["ticket_id"]:
                raise ValueError(
                    "Ticket risk must include ticket_id."
                )

            if not risk["quote"]:
                raise ValueError(
                    "Ticket risk must include a direct quote."
                )

class TAMSummarizer:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)
        self.loader = AccountLoader()

        self.prompt_template = Path(
            "prompts/tam_v1.txt"
        ).read_text(encoding="utf-8")

    def summarize(self, account_id: str) -> AccountBrief:
        context = self.loader.get_account_context(account_id)

        account = context["account"]
        tickets = context["tickets"]

        risks = detect_account_risks(
            account,
            tickets,
        )

        account_json = json.dumps(
            account,
            indent=2,
            ensure_ascii=False,
        )

        tickets_json = json.dumps(
            tickets,
            indent=2,
            ensure_ascii=False,
        )

        risks_json = json.dumps(
            risks,
            indent=2,
            ensure_ascii=False,
        )

        prompt = (
            self.prompt_template
            .replace("{account}", account_json)
            .replace("{tickets}", tickets_json)
            .replace("{risks}", risks_json)
        )

        response = self.client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config={
                "temperature": 0,
                "response_mime_type": "application/json",
            },
        )

        data = json.loads(response.text)

        validate_brief_output(data)

        open_risks = []

        for risk in data.get("open_risks", []):
            open_risks.append(
                RiskFlag(
                    risk_type=risk["risk_type"],
                    source=risk["source"],
                    evidence=risk["evidence"],
                    ticket_id=risk.get("ticket_id"),
                    quote=risk.get("quote"),
                )
            )

        return AccountBrief(
            executive_summary=data["executive_summary"],
            open_risks=open_risks,
            talking_points=data["talking_points"],
        )