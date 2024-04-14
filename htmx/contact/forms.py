from django import forms

from htmx.contact.models import Contact


class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "phone", "email"]
