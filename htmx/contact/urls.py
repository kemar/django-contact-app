from django.urls import path

from htmx.contact import views


app_name = "contact"  # URL namespace.

urlpatterns = [
    path("", views.list, name="list"),
    path("new", views.create, name="create"),
    path("<int:pk>", views.detail, name="detail"),
    path("<int:pk>/edit", views.update, name="update"),
    path("<int:pk>/delete", views.delete, name="delete"),
    path("<int:pk>/email", views.email, name="email"),
    path("count", views.count, name="count"),
    path("delete/all", views.delete_all, name="delete_all"),
    path("archive/download", views.archive_download_trigger, name="archive_download_trigger"),
    path("archive/monitor/<int:task_id>", views.archive_download_monitor, name="archive_download_monitor"),
]
