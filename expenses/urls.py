
from django.urls import path
from . import views

app_name = "expenses"

urlpatterns = [
    path(
        "groups/",
        views.group_list,
        name="group_list"
    ),
    path(
        "groups/create/",
        views.group_create,
        name="group_create"
    ),
    path(
        "groups/<int:pk>/",
        views.group_detail,
        name="group_detail"
    ),
    path(
        "groups/<int:pk>/edit/",
        views.group_edit,
        name="group_edit"
    ),
    path(
        "groups/<int:pk>/delete/",
        views.group_delete,
        name="group_delete"
    ),
    path(
        "groups/<int:pk>/members/add/",
        views.group_add_member,
        name="group_add_member"
    ),
]
