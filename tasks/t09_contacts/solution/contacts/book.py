"""Contact book management."""
from contacts.contact import Contact, normalize_phone


class ContactBook:
    def __init__(self):
        self._contacts = []

    def add(self, contact):
        for existing in self._contacts:
            if existing.name.lower() == contact.name.lower():
                return existing
        self._contacts.append(contact)
        return contact

    def remove(self, name):
        self._contacts = [c for c in self._contacts if c.name.lower() != name.lower()]

    def get(self, name):
        for c in self._contacts:
            if c.name.lower() == name.lower():
                return c
        return None

    def all_contacts(self):
        return sorted(self._contacts, key=lambda c: c.name.lower())

    def merge_duplicates(self):
        merged = {}
        for contact in self._contacts:
            key = contact.name.lower()
            if key not in merged:
                merged[key] = Contact(
                    name=contact.name,
                    phones=list(contact.phones),
                    emails=list(contact.emails),
                )
            else:
                target = merged[key]
                for p in contact.phones:
                    target.add_phone(p)
                for e in contact.emails:
                    target.add_email(e)
        self._contacts = sorted(merged.values(), key=lambda c: c.name.lower())

    def __len__(self):
        return len(self._contacts)
