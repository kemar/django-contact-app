from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from htmx.contact.forms import ContactModelForm
from htmx.contact.models import Contact


@require_http_methods(["GET"])
def list(request):
    query = request.GET.get("q")
    contacts_set = Contact.objects.search(query) if query else Contact.objects.all()
    context = {"contacts": contacts_set}
    return render(request, "contact/list.html", context)


@require_http_methods(["GET", "POST"])
def create(request):
    form = ContactModelForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Created New Contact!")
        return HttpResponseRedirect(reverse("contact:list"))

    context = {"form": form}
    return render(request, "contact/create.html", context)


@require_http_methods(["GET"])
def detail(request, pk: int):
    contact = get_object_or_404(Contact, pk=pk)

    context = {"contact": contact}
    return render(request, "contact/detail.html", context)


@require_http_methods(["GET", "POST"])
def update(request, pk: int):
    contact = get_object_or_404(Contact, pk=pk)
    form = ContactModelForm(request.POST or None, instance=contact)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Updated Contact!")
        return HttpResponseRedirect(reverse("contact:list"))

    context = {"form": form, "contact": contact}
    return render(request, "contact/update.html", context)


@require_http_methods(["POST"])
def delete(request, pk: int):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    messages.success(request, "Deleted Contact!")
    return HttpResponseRedirect(reverse("contact:list"))
