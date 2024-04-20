from django import forms
from django.urls import reverse

from htmx.contact.models import Contact


class ContactModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["email"].widget.attrs["hx-get"] = reverse("contact:email", args=[self.instance.pk])
            self.fields["email"].widget.attrs["hx-target"] = "next .errorlist"
            # `changed` causes the input to not issue HTTP requests unless the value is actually changed.
            self.fields["email"].widget.attrs["hx-trigger"] = "change, keyup delay:200ms changed"

    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "phone", "email"]
