"""Import and export contacts as CSV."""
import csv
import io
from contacts.contact import Contact


def export_csv(contacts):
    """Export contacts to CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["name", "phones", "emails"])
    for c in contacts:
        phones = ";".join(c.phones)
        emails = ";".join(c.emails)
        writer.writerow([c.name, phones, emails])
    return output.getvalue().rstrip("\r\n")


def import_csv(text):
    """Import contacts from CSV string."""
    contacts = []
    reader = csv.reader(io.StringIO(text.strip()))
    header = next(reader, None)
    for row in reader:
        if len(row) < 3:
            continue
        name = row[0].strip()
        phones = [p.strip() for p in row[1].split(";") if p.strip()]
        emails = [e.strip() for e in row[2].split(";") if e.strip()]
        c = Contact(name=name)
        for p in phones:
            c.add_phone(p)
        for e in emails:
            c.add_email(e)
        contacts.append(c)
    return contacts
