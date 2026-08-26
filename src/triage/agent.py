import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from src.retrieval.retriever import KBRetriever
from src.triage.schemas import KBReference, TriageResult


load_dotenv()
def validate_triage_output(data: dict) -> None:
    """Validate the LLM's structured triage response."""

    required_fields = {
        "product_area",
        "issue_category",
        "urgency",
        "urgency_reason",
        "reasoning",
        "known_issue",
        "kb_reference",
        "responder_team",
        "first_response",
    }

    missing = required_fields - data.keys()

    if missing:
        raise ValueError(
            f"Missing required triage fields: {sorted(missing)}"
        )

    valid_categories = {
        "Bug",
        "Feature Request",
        "How-To",
        "Performance",
        "Billing",
        "Integration",
        "Onboarding",
        "Data Loss",
    }

    valid_urgencies = {"P1", "P2", "P3", "P4"}

    if data["issue_category"] not in valid_categories:
        raise ValueError(
            f"Invalid issue category: {data['issue_category']}"
        )

    if data["urgency"] not in valid_urgencies:
        raise ValueError(
            f"Invalid urgency: {data['urgency']}"
        )

    if not isinstance(data["known_issue"], bool):
        raise ValueError("known_issue must be boolean.")

    if not isinstance(data["first_response"], str):
        raise ValueError("first_response must be a string.")

    if data["known_issue"]:
        if not isinstance(data["kb_reference"], dict):
            raise ValueError(
                "kb_reference is required when known_issue is true."
            )

        required_kb_fields = {
            "source",
            "section",
            "relevance_score",
        }

        missing_kb = required_kb_fields - data["kb_reference"].keys()

        if missing_kb:
            raise ValueError(
                f"Missing KB reference fields: {sorted(missing_kb)}"
            )

class TriageAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)
        self.retriever = KBRetriever()

        self.prompt_template = Path(
            "prompts/triage_v1.txt"
        ).read_text(encoding="utf-8")

    def triage(self, subject: str, body: str) -> TriageResult:
        ticket_text = f"{subject}\n\n{body}"

        kb_results = [
    result
    for result in self.retriever.search(ticket_text, top_k=3)
    if result["score"] >= 0.15
]

        kb_context = "\n\n".join(
            [
                (
                    f"Source: {result['source']}\n"
                    f"Section: {result['section']}\n"
                    f"Relevance: {result['score']}\n"
                    f"Content:\n{result['text']}"
                )
                for result in kb_results
            ]
        )

        prompt = (
            self.prompt_template
            .replace("{subject}", subject)
            .replace("{body}", body)
            .replace("{kb_context}", kb_context)
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
        validate_triage_output(data)
        kb_reference = None

        if data.get("known_issue") and data.get("kb_reference"):
            ref = data["kb_reference"]

            kb_reference = KBReference(
                source=ref["source"],
                section=ref["section"],
                relevance_score=float(ref["relevance_score"]),
            )

        return TriageResult(
            product_area=data["product_area"],
            issue_category=data["issue_category"],
            urgency=data["urgency"],
            urgency_reason=data["urgency_reason"],
            reasoning=data["reasoning"],
            known_issue=data["known_issue"],
            kb_reference=kb_reference,
            responder_team=data["responder_team"],
            first_response=data["first_response"],
        )
        
    def triage_ticket(subject: str, body: str) -> TriageResult:
        """
    Public callable interface for Task 1.

    Accepts a raw support ticket and returns a validated
    structured triage result.
    """
        agent = TriageAgent()
        return agent.triage(subject, body)
        