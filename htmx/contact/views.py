import asyncio

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import QueryDict
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseRedirectBase, StreamingHttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from htmx.contact.forms import ContactModelForm
from htmx.contact.models import Contact


class HttpResponseRedirect303(HttpResponseRedirectBase):
    status_code = 303


@require_http_methods(["GET"])
def list(request):
    is_htmx_search_trigger = request.META.get("HTTP_HX_TRIGGER") == "search"
    is_hyperview = "X-Hyperview-Version" in request.headers
    is_hyperview_rows_only = is_hyperview and request.GET.get("rows_only")

    query = request.GET.get("q")
    page_number = request.GET.get("page")

    contacts_set = Contact.objects.search(query) if query else Contact.objects.all()
    paginator = Paginator(contacts_set.order_by("last_name"), 10)
    contacts_page = paginator.get_page(page_number)

    context = {"contacts_page": contacts_page}

    if is_htmx_search_trigger or is_hyperview_rows_only:
        if is_hyperview_rows_only:
            return render(request, "contact_mobile/rows.xml", context, content_type="application/vnd.hyperview+xml")
        return render(request, "contact/includes/list_rows.html", context)

    if is_hyperview:
        return render(request, "contact_mobile/index.xml", context, content_type="application/vnd.hyperview+xml")
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
    is_hyperview = "X-Hyperview-Version" in request.headers

    if is_hyperview:
        return render(request, "contact_mobile/show.xml", context, content_type="application/vnd.hyperview+xml")
    return render(request, "contact/detail.html", context)


@require_http_methods(["GET", "POST"])
def update(request, pk: int):
    is_hyperview = "X-Hyperview-Version" in request.headers

    contact = get_object_or_404(Contact, pk=pk)
    form = ContactModelForm(request.POST or None, instance=contact)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Updated Contact!")
        if is_hyperview:
            context = {"form": form, "contact": contact, "saved": True}
            # See: "Why Not Redirect?" (https://github.com/bigskysoftware/hypermedia-systems/blob/ab7dd0a149972465015ebe9fbee91706ba93cfe4/book/CH12_BuildingAContactsAppWithHyperview.adoc?plain=1#L761-L780)
            return render(
                request, "contact_mobile/form_fields.xml", context, content_type="application/vnd.hyperview+xml"
            )
        return HttpResponseRedirect(reverse("contact:list"))

    context = {"form": form, "contact": contact}
    if is_hyperview:
        if form.errors:
            # HXML will replace `form_fields.xml` only so that the UI will
            # remain in the editing mode to show error messages.
            return render(
                request, "contact_mobile/form_fields.xml", context, content_type="application/vnd.hyperview+xml"
            )
        return render(request, "contact_mobile/edit.xml", context, content_type="application/vnd.hyperview+xml")
    return render(request, "contact/update.html", context)


# We need to support POST in addition to DELETE, since the Hyperview client only understands GET and POST.
# https://hyperview.org/docs/reference_behavior_attributes#verb
@require_http_methods(["POST", "DELETE"])
def delete(request, pk: int):
    is_hyperview = "X-Hyperview-Version" in request.headers

    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()

    if request.META.get("HTTP_HX_TRIGGER") == "delete-btn":
        messages.success(request, "Deleted Contact!")
        return HttpResponseRedirect303(reverse("contact:list"))

    if is_hyperview:
        return render(request, "contact_mobile/delete.xml", {}, content_type="application/vnd.hyperview+xml")
    return HttpResponse("")


@require_http_methods(["GET"])
def email(request, pk: int):
    """
    Inline validation of email uniqueness.
    """
    contact = get_object_or_404(Contact, pk=pk)
    try:
        contact.email = request.GET.get("email")
        contact.validate_unique()
        return HttpResponse("")
    except ValidationError as e:
        return HttpResponse(e.error_dict["email"][0])


@require_http_methods(["GET"])
async def count(request):
    """
    This is a free and performant operation via `paginator.count`.

    But we assume that creating a count string is an expensive and slow
    operation for the sake of demonstrating htmx lazy loading.
    """
    count = await Contact.objects.acount()
    await asyncio.sleep(3)  # Simulate a slow operation.
    return HttpResponse(f"({count} total Contacts)")


@require_http_methods(["DELETE"])
def delete_all(request):
    """
    Bulk delete contacts.
    """
    contact_ids = QueryDict(request.body).getlist("selected_contact_ids")
    Contact.objects.filter(id__in=contact_ids).delete()
    messages.success(request, "Deleted Contacts!")
    return HttpResponseRedirect303(reverse("contact:list"))


@require_http_methods(["POST"])
def archive_download_trigger(request):
    """
    Asynchronous task start simulation.
    """
    # Here, you would trigger an async task via whatever you have available.
    # And then, just return its ID.
    context = {"task_id": 1}
    return render(request, "contact/includes/archive_download_ui.html", context)


@require_http_methods(["GET"])
def archive_download_monitor(request, task_id: int):
    """
    Asynchronous task monitoring simulation (via Server-Sent Events).
    """

    # Here, you would do something allowing to track the status of the process,
    # like `task = get_async_task(task_id)`.

    async def server_sent_event_stream(task_id):
        # Here, different actions could be performed depending on `task.status`.

        # This simulates an async task that takes 10 seconds.
        for i in range(1, 11):
            await asyncio.sleep(1)
            event = f"event: progress-{task_id}\n"
            data = f'data: <progress max="100" value="{i * 10}"></progress> {i * 10} %\n'
            yield f"{event}{data}\n"

        # The task is done and we return a link to its result.
        # We also swap the parent element to gracefully close the HTTP connection.
        # https://github.com/bigskysoftware/htmx/issues/2393
        event = f"event: progress-{task_id}\n"
        data = (
            'data: <a href="/static/img/task_result.jpg" '
            'download id="sse-listener" hx-swap-oob="true">'
            "Download</a>\n"
        )
        yield f"{event}{data}\n"

    return StreamingHttpResponse(
        streaming_content=server_sent_event_stream(task_id),
        content_type="text/event-stream",
    )
