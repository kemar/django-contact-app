from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    # Redirect "/" to display a list of contacts as the root page.
    path("", RedirectView.as_view(url="contact/", permanent=False)),
    # Contact URLs.
    path("contact/", include("htmx.contact.urls")),
]
