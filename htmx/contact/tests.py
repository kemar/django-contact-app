from django.test import TestCase

from htmx.contact.models import Contact


class ContactTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.john = Contact.objects.create(first_name="John", last_name="Doe", email="john@doe.com")
        cls.jane = Contact.objects.create(first_name="Jane", last_name="Doe", email="jane@doe.com")

    def test_delete_contact(self):
        """
        Contact is correctly deleted.
        """
        assert Contact.objects.count() == 2

        response = self.client.delete(f"/contact/{self.john.id}/delete")
        assert response.status_code == 303

        assert Contact.objects.count() == 1

    def test_contact_email_inline_validation(self):
        """
        Email is correctly validated.
        """
        response = self.client.get(f"/contact/{self.john.id}/email?email={self.john.email}")
        assert response.status_code == 200
        assert response.content == b""

        response = self.client.get(f"/contact/{self.john.id}/email?email={self.jane.email}")
        assert response.status_code == 200
        assert response.content == b"Contact with this Email already exists."

    def test_update_template(self):
        """
        Template for update contains necessary elements and HTMX attributes.
        """
        response = self.client.get(f"/contact/{self.john.id}/edit")
        assert response.status_code == 200
        assert b'hx-get="/contact/1/email"' in response.content
        assert b'hx-target="next .errorlist"' in response.content
        assert b'hx-trigger="change, keyup delay:200ms changed"' in response.content
        assert b'<p class="errorlist"></p>' in response.content
