import unittest
from contacts.contact import Contact
from contacts.book import ContactBook


class BasicTest(unittest.TestCase):
    def test_add_and_get(self):
        book = ContactBook()
        c = Contact(name="Alice")
        book.add(c)
        self.assertEqual(book.get("Alice").name, "Alice")

    def test_contact_phone(self):
        c = Contact(name="Bob")
        c.add_phone("555-1234")
        self.assertEqual(len(c.phones), 1)


if __name__ == "__main__":
    unittest.main()
