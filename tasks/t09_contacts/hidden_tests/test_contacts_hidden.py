import unittest

from contacts.contact import Contact, normalize_phone
from contacts.book import ContactBook
from contacts.search import search_by_name, search_by_phone, search_by_email
from contacts.io_csv import export_csv, import_csv


class PhoneNormalizationHidden(unittest.TestCase):
    def test_country_code_preserved(self):
        self.assertEqual(normalize_phone("+1-555-1234"), "15551234")
        self.assertEqual(normalize_phone("+44-20-7946-0958"), "442079460958")

    def test_plain_number(self):
        self.assertEqual(normalize_phone("555-1234"), "5551234")


class DuplicateDetectionHidden(unittest.TestCase):
    def test_case_insensitive_add(self):
        book = ContactBook()
        book.add(Contact(name="Alice"))
        book.add(Contact(name="alice"))
        self.assertEqual(len(book), 1)

    def test_case_insensitive_get(self):
        book = ContactBook()
        book.add(Contact(name="Alice"))
        self.assertIsNotNone(book.get("alice"))
        self.assertEqual(book.get("ALICE").name, "Alice")

    def test_case_insensitive_remove(self):
        book = ContactBook()
        book.add(Contact(name="Alice"))
        book.remove("ALICE")
        self.assertEqual(len(book), 0)


class SearchHidden(unittest.TestCase):
    def test_partial_name_match(self):
        contacts = [Contact(name="Alice Smith"), Contact(name="Bob Jones")]
        results = search_by_name(contacts, "ali")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Alice Smith")

    def test_partial_name_case_insensitive(self):
        contacts = [Contact(name="Alice Smith"), Contact(name="Alicia Keys")]
        results = search_by_name(contacts, "ALIC")
        self.assertEqual(len(results), 2)

    def test_search_by_phone_and_email(self):
        c = Contact(name="Alice")
        c.add_phone("+1-555-1234")
        c.add_email("Alice@Example.com")
        self.assertEqual(len(search_by_phone([c], "15551234")), 1)
        self.assertEqual(len(search_by_email([c], "alice@example.com")), 1)


class CsvExportHidden(unittest.TestCase):
    def test_commas_in_name(self):
        c = Contact(name="Doe, Jane")
        c.add_phone("555-1234")
        c.add_email("jane@example.com")
        csv_text = export_csv([c])
        imported = import_csv(csv_text)
        self.assertEqual(len(imported), 1)
        self.assertEqual(imported[0].name, "Doe, Jane")

    def test_round_trip(self):
        c1 = Contact(name="Alice")
        c1.add_phone("555-1111")
        c1.add_email("a@b.com")
        c2 = Contact(name="Bob")
        c2.add_phone("555-2222")
        c2.add_email("b@c.com")
        csv_text = export_csv([c1, c2])
        imported = import_csv(csv_text)
        self.assertEqual(len(imported), 2)
        names = {c.name for c in imported}
        self.assertEqual(names, {"Alice", "Bob"})


class CsvImportHidden(unittest.TestCase):
    def test_last_record_not_skipped(self):
        csv_text = "name,phones,emails\nAlice,555-1111,a@b.com\nBob,555-2222,b@c.com\n"
        imported = import_csv(csv_text)
        self.assertEqual(len(imported), 2)
        names = [c.name for c in imported]
        self.assertIn("Bob", names)

    def test_single_record(self):
        csv_text = "name,phones,emails\nAlice,555-1111,a@b.com\n"
        imported = import_csv(csv_text)
        self.assertEqual(len(imported), 1)


class MergeDuplicatesHidden(unittest.TestCase):
    def test_merge_combines_contacts(self):
        book = ContactBook()
        c1 = Contact(name="Alice", phones=["555-1111"], emails=["a@b.com"])
        c2 = Contact(name="alice", phones=["555-2222"], emails=["a2@b.com"])
        book._contacts.append(c1)
        book._contacts.append(c2)
        book.merge_duplicates()
        self.assertEqual(len(book), 1)
        merged = book.all_contacts()[0]
        self.assertEqual(len(merged.phones), 2)
        self.assertEqual(len(merged.emails), 2)

    def test_merge_keeps_first_name(self):
        book = ContactBook()
        book._contacts.append(Contact(name="Alice"))
        book._contacts.append(Contact(name="ALICE"))
        book.merge_duplicates()
        self.assertEqual(book.all_contacts()[0].name, "Alice")

    def test_merge_deduplicates_phones(self):
        book = ContactBook()
        book._contacts.append(Contact(name="Alice", phones=["555-1111"]))
        book._contacts.append(Contact(name="alice", phones=["555-1111"]))
        book.merge_duplicates()
        self.assertEqual(len(book.all_contacts()[0].phones), 1)


if __name__ == "__main__":
    unittest.main()
