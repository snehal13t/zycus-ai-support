import json
from datetime import datetime, timedelta
from pathlib import Path


class AccountLoader:
    def __init__(
        self,
        accounts_path: str = "data/accounts.json",
        tickets_path: str = "data/tickets.json",
    ):
        self.accounts = json.loads(
            Path(accounts_path).read_text(encoding="utf-8")
        )

        self.tickets = json.loads(
            Path(tickets_path).read_text(encoding="utf-8")
        )

        self.account_map = {
            account["account_id"]: account
            for account in self.accounts
        }

    def get_account(self, account_id: str) -> dict:
        """Return account summary for the given account ID."""

        account = self.account_map.get(account_id)

        if not account:
            raise ValueError(
                f"Account not found: {account_id}"
            )

        return account

    def get_recent_tickets(
        self,
        account_id: str,
        days: int = 90,
    ) -> list[dict]:
        """
        Return tickets for an account within the last `days`
        relative to the latest ticket timestamp in the dataset.
        """

        if not self.tickets:
            return []

        # The dataset has its own synthetic timeline.
        # Anchor the 90-day window to the latest ticket in
        # the provided dataset rather than the machine's current date.
        latest_ticket_date = max(
            datetime.fromisoformat(
                ticket["created_at"].replace("Z", "+00:00")
            )
            for ticket in self.tickets
        )

        cutoff = latest_ticket_date - timedelta(days=days)

        tickets = []

        for ticket in self.tickets:
            if ticket["account_id"] != account_id:
                continue

            created_at = datetime.fromisoformat(
                ticket["created_at"].replace("Z", "+00:00")
            )

            if created_at >= cutoff:
                tickets.append(ticket)

        return sorted(
            tickets,
            key=lambda ticket: ticket["created_at"],
            reverse=True,
        )

    def get_account_context(
        self,
        account_id: str,
        days: int = 90,
    ) -> dict:
        """Return account summary plus recent ticket history."""

        return {
            "account": self.get_account(account_id),
            "tickets": self.get_recent_tickets(
                account_id,
                days,
            ),
        }