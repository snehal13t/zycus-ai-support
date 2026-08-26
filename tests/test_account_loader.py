from src.tam.account_loader import AccountLoader


loader = AccountLoader()

account_id = "ACC-3336"

context = loader.get_account_context(account_id)

account = context["account"]
tickets = context["tickets"]

print("=" * 70)
print("ACCOUNT")
print("=" * 70)

print("Account ID:", account["account_id"])
print("Company:", account["company"])
print("TAM:", account["tam"])
print("Plan:", account["plan_tier"])
print("Health:", account["health_status"])
print("Usage Trend:", account["usage_trend"])
print("Open Tickets:", account["open_tickets"])
print("P1 Tickets (30d):", account["p1_tickets_last_30d"])
print("ARR:", account["arr_usd"])

print("\n" + "=" * 70)
print("LAST 90 DAYS TICKETS")
print("=" * 70)

print("Ticket count:", len(tickets))

for ticket in tickets[:5]:
    print("\n", ticket["ticket_id"])
    print("Subject:", ticket["subject"])
    print("Status:", ticket["status"])
    print("Urgency:", ticket["urgency"])
    print("Created:", ticket["created_at"])