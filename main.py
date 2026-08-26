import json
import sys
from pathlib import Path

from src.tam.summarizer import TAMSummarizer
from src.triage.agent import TriageAgent


def load_tickets():
    return json.loads(
        Path("data/tickets.json").read_text(
            encoding="utf-8"
        )
    )


def run_task1():
    tickets = load_tickets()

    ticket = tickets[0]

    agent = TriageAgent()

    result = agent.triage(
        subject=ticket["subject"],
        body=ticket["body"],
    )

    print("\n" + "=" * 70)
    print("TASK 1 — INTELLIGENT TICKET TRIAGE")
    print("=" * 70)

    print(f"\nTicket: {ticket['ticket_id']}")
    print(f"Subject: {ticket['subject']}")

    print("\nClassification")
    print(f"Product Area: {result.product_area}")
    print(f"Issue Category: {result.issue_category}")
    print(f"Urgency: {result.urgency}")

    print("\nKnown Issue")
    print(result.known_issue)

    print("\nResponder Team")
    print(result.responder_team)

    print("\nFirst Response")
    print(result.first_response)


def run_task2():
    account_id = "ACC-7397"

    summarizer = TAMSummarizer()
    brief = summarizer.summarize(account_id)

    print("\n" + "=" * 70)
    print("TASK 2 — TAM ACCOUNT HEALTH SUMMARY")
    print("=" * 70)

    print(f"\nAccount: {account_id}")

    print("\nExecutive Summary")
    print(brief.executive_summary)

    print("\nOpen Risks")

    if not brief.open_risks:
        print("No significant risks identified.")
    else:
        for risk in brief.open_risks:
            print(f"- {risk.risk_type}: {risk.evidence}")

            if risk.ticket_id:
                print(f"  Ticket: {risk.ticket_id}")

            if risk.quote:
                print(f'  Quote: "{risk.quote}"')

    print("\nRecommended Talking Points")

    for point in brief.talking_points:
        print(f"- {point}")


def main():
    if len(sys.argv) == 1:
        print("Zycus AI Support Assistant")
        print("\nUsage:")
        print("  python main.py triage")
        print("  python main.py tam")
        print("  python main.py demo")

        return

    command = sys.argv[1].lower()

    if command == "triage":
        run_task1()

    elif command == "tam":
        run_task2()

    elif command == "demo":
        run_task1()
        run_task2()

    else:
        print(f"Unknown command: {command}")
        print("Use: triage, tam, or demo")
        sys.exit(1)


if __name__ == "__main__":
    main()