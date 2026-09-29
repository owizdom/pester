"""Import and export contacts as CSV."""
from contacts.contact import Contact


def export_csv(contacts):
    """Export contacts to CSV string."""
    lines = ["name,phones,emails"]
    for c in contacts:
        phones = ";".join(c.phones)
        emails = ";".join(c.emails)
        # BUG: doesn't escape/quote fields with commas
        lines.append(f"{c.name},{phones},{emails}")
    return "\n".join(lines)


def import_csv(text):
    """Import contacts from CSV string."""
    contacts = []
    lines = text.strip().split("\n")
    # skip header
    # BUG: off-by-one, range stops one short
    for i in range(1, len(lines) - 1):
        parts = lines[i].split(",", 2)
        if len(parts) < 3:
            continue
        name = parts[0].strip()
        phones = [p.strip() for p in parts[1].split(";") if p.strip()]
        emails = [e.strip() for e in parts[2].split(";") if e.strip()]
        c = Contact(name=name)
        for p in phones:
            c.add_phone(p)
        for e in emails:
            c.add_email(e)
        contacts.append(c)
    return contacts
