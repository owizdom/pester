"""Search contacts by various criteria."""


def search_by_name(contacts, query):
    """Search contacts by name. Should support partial matching."""
    results = []
    for contact in contacts:
        # BUG: exact match only, should be partial/substring
        if contact.name == query:
            results.append(contact)
    return results


def search_by_phone(contacts, phone):
    """Search contacts that have this phone number."""
    from contacts.contact import normalize_phone
    target = normalize_phone(phone)
    results = []
    for contact in contacts:
        for p in contact.phones:
            if normalize_phone(p) == target:
                results.append(contact)
                break
    return results


def search_by_email(contacts, email):
    """Search contacts that have this email."""
    results = []
    for contact in contacts:
        for e in contact.emails:
            if e.lower() == email.lower():
                results.append(contact)
                break
    return results
