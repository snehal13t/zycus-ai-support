import json

from src.triage.agent import TriageAgent


with open("data/tickets.json", "r", encoding="utf-8") as f:
    tickets = json.load(f)

ticket = tickets[0]

agent = TriageAgent()

result = agent.triage(
    subject=ticket["subject"],
    body=ticket["body"],
)

print("\n" + "=" * 70)
print("TASK 1 — TRIAGE RESULT")
print("=" * 70)

print(f"\nTicket ID: {ticket['ticket_id']}")
print(f"Subject: {ticket['subject']}")

print("\n--- Classification ---")
print("Product Area:", result.product_area)
print("Issue Category:", result.issue_category)
print("Urgency:", result.urgency)

print("\n--- Reasoning ---")
print(result.reasoning)

print("\n--- Urgency Reason ---")
print(result.urgency_reason)

print("\n--- Known Issue ---")
print(result.known_issue)

if result.kb_reference:
    print("\n--- KB Reference ---")
    print("Source:", result.kb_reference.source)
    print("Section:", result.kb_reference.section)
    print("Score:", result.kb_reference.relevance_score)

print("\n--- Responder Team ---")
print(result.responder_team)

print("\n--- First Response ---")
print(result.first_response)