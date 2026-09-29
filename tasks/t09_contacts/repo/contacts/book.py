"""Contact book management."""
from contacts.contact import Contact


class ContactBook:
    def __init__(self):
        self._contacts = []

    def add(self, contact):
        # BUG: case-sensitive duplicate check
        for existing in self._contacts:
            if existing.name == contact.name:
                return existing
        self._contacts.append(contact)
        return contact

    def remove(self, name):
        self._contacts = [c for c in self._contacts if c.name != name]

    def get(self, name):
        for c in self._contacts:
            if c.name == name:
                return c
        return None

    def all_contacts(self):
        return sorted(self._contacts, key=lambda c: c.name.lower())

    def __len__(self):
        return len(self._contacts)
