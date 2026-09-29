"""Contact data model."""
from dataclasses import dataclass, field


def normalize_phone(raw):
    """Strip non-digit characters from a phone number."""
    digits = "".join(c for c in raw if c.isdigit())
    # BUG: strips leading country code by removing first digit when '+' present
    if raw.startswith("+"):
        digits = digits[1:]
    return digits


@dataclass
class Contact:
    name: str
    phones: list = field(default_factory=list)
    emails: list = field(default_factory=list)

    def add_phone(self, phone):
        normalized = normalize_phone(phone)
        if normalized not in [normalize_phone(p) for p in self.phones]:
            self.phones.append(phone)

    def add_email(self, email):
        if email.lower() not in [e.lower() for e in self.emails]:
            self.emails.append(email)
