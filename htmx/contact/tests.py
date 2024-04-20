from django.test import TestCase

from htmx.contact.models import Contact


class ContactTestCase(TestCase):
    def test_delete_contact(self):
        """
        Contact is correctly deleted.
        """
        contact = Contact.objects.create(first_name="John", last_name="Doe", email="john@doe.com")
        assert Contact.objects.count() == 1

        response = self.client.delete(f"/contact/{contact.id}/delete")
        assert response.status_code == 303

        assert Contact.objects.count() == 0
