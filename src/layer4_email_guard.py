"""
Layer 4: Rule-Based Action Check for Email (Eq. 4).
Implements:
  Allow(e) = 1 if domain(e) in D; otherwise 0
where D is the set of approved internal company domains.
Nothing real is ever sent; approved actions write only to a local sandbox log file.
"""

import os
from datetime import datetime, timezone

APPROVED_DOMAINS = {"company-hr.example.com", "internal.example.com"}


def extract_domain(email_address: str) -> str:
    if "@" not in email_address:
        return ""
    return email_address.strip().split("@")[-1].lower().rstrip(".,;)")


def allow_email(email_address: str, approved_domains: set[str] = APPROVED_DOMAINS) -> int:
    """Eq. (4): Allow(e) = 1 if domain(e) in D; otherwise 0."""
    domain = extract_domain(email_address)
    return 1 if domain in approved_domains else 0


class EmailActionGuard:
    def __init__(self, enabled: bool = True, log_path: str = None):
        self.enabled = enabled
        self.log_path = log_path or os.path.join(
            os.path.dirname(__file__), "..", "results", "sandbox_email.log"
        )
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def send_email_sandbox(self, recipient: str, subject: str, body: str) -> dict:
        timestamp = datetime.now(timezone.utc).isoformat()
        if self.enabled:
            allowed_flag = allow_email(recipient)
            if allowed_flag == 0:
                entry = (
                    f"[{timestamp}] BLOCKED (Layer 4) | To: {recipient} | "
                    f"Reason: Domain '{extract_domain(recipient)}' not in D={sorted(list(APPROVED_DOMAINS))}\n"
                )
                with open(self.log_path, "a", encoding="utf-8") as f:
                    f.write(entry)
                return {
                    "sent": False,
                    "blocked_by_layer4": True,
                    "recipient": recipient,
                    "reason": f"Unapproved domain '{extract_domain(recipient)}'",
                }

        entry = f"[{timestamp}] SENT (SANDBOX LOG ONLY) | To: {recipient} | Subject: {subject}\n"
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(entry)
        return {
            "sent": True,
            "blocked_by_layer4": False,
            "recipient": recipient,
            "reason": "Allowed",
        }
