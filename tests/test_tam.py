from src.tam.summarizer import TAMSummarizer


summarizer = TAMSummarizer()

account_id = "ACC-7397"

brief = summarizer.summarize(account_id)

print("\n" + "=" * 70)
print("TASK 2 — TAM ACCOUNT HEALTH BRIEF")
print("=" * 70)

print("\n--- EXECUTIVE SUMMARY ---")
print(brief.executive_summary)

print("\n--- OPEN RISKS & FLAGGED ISSUES ---")

if not brief.open_risks:
    print("No significant risks identified.")
else:
    for risk in brief.open_risks:
        print(f"\nRisk Type: {risk.risk_type}")
        print(f"Source: {risk.source}")
        print(f"Evidence: {risk.evidence}")

        if risk.ticket_id:
            print(f"Ticket ID: {risk.ticket_id}")

        if risk.quote:
            print(f"Quote: \"{risk.quote}\"")

print("\n--- RECOMMENDED TALKING POINTS ---")

for i, point in enumerate(brief.talking_points, 1):
    print(f"{i}. {point}")