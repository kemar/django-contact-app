from django.template import Context, Template
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

        response = self.client.delete(f"/contact/{self.john.id}/delete", headers={"HX_TRIGGER": "delete-btn"})
        assert response.status_code == 303

        assert Contact.objects.count() == 1

    def test_inline_delete_contact(self):
        """
        Contact is correctly inline deleted.
        """
        assert Contact.objects.count() == 2

        response = self.client.delete(f"/contact/{self.john.id}/delete")
        assert response.status_code == 200
        assert response.content == b""

        assert Contact.objects.count() == 1

    def test_bulk_delete_contacts(self):
        """
        Contacts are correctly bulk deleted.
        """
        assert Contact.objects.count() == 2

        body = f"selected_contact_ids={self.john.id}&selected_contact_ids={self.jane.id}"
        response = self.client.delete("/contact/delete/all", body)
        assert response.status_code == 303

        assert Contact.objects.count() == 0

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

    def test_list_template(self):
        """
        Template for list contains necessary HTMX attributes.
        """
        for i in range(5):
            Contact.objects.create(first_name=f"foo{i}", last_name=f"bar{i}", email=f"baz{i}@foo.bar")

        response = self.client.get("/contact/")
        assert response.status_code == 200
        self.assertTemplateUsed(response, "contact/list.html")

    def test_list_template_partial(self):
        """
        Partial template is correctly used
        """
        response = self.client.get("/contact/?q=a", headers={"HX_TRIGGER": "search"})
        assert response.status_code == 200
        self.assertTemplateUsed(response, "contact/includes/list_rows.html")

    def test_url_add_query(self):
        """
        Test `url_add_query` template tag.
        """

        context = {"url": "https://foo.com/contact/?q=a&page=2"}
        template = Template("{% load url_add_query %}{% url_add_query url page=3 %}")
        out = template.render(Context(context))
        assert out == "https://foo.com/contact/?q=a&amp;page=3"

        # Relative URL.
        context = {"url": "contact/?q=a&page=2"}
        template = Template("{% load url_add_query %}{% url_add_query url page=3 %}")
        out = template.render(Context(context))
        assert out == "contact/?q=a&amp;page=3"

        # Empty URL.
        context = {"url": ""}
        template = Template("{% load url_add_query %}{% url_add_query url page=3 %}")
        out = template.render(Context(context))
        assert out == "?page=3"
