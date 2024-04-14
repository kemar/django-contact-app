from django.db import models
from django.db.models import Q


class ContactManager(models.Manager):
    def search(self, query):
        return self.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(phone__icontains=query)
            | Q(email__icontains=query)
        )


class Contact(models.Model):
    first_name = models.CharField(verbose_name="First name", max_length=255)
    last_name = models.CharField(verbose_name="Last name", max_length=255)
    phone = models.CharField(verbose_name="Phone", max_length=255, blank=True)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)

    objects = ContactManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"
