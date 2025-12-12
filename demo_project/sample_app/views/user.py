from django.contrib.auth.models import Group, User

from classy_admin.views import (
    CreateView,
    DeleteView,
    DetailView,
    TableListView,
    UpdateView,
)
from classy_admin.viewsets import ViewSet

user_vs = ViewSet(User)
group_vs = ViewSet(Group)


@user_vs.action("list")
class UserListView(TableListView):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "last_login",
        "is_active",
        "is_staff",
        "is_superuser",
    ]


class UserFormMixin:
    fields = [
        "username",
        "first_name",
        "last_name",
        "last_login",
        "is_active",
        "is_staff",
        "is_superuser",
    ]


@user_vs.action("add")
class UserCreateView(UserFormMixin, CreateView):
    pass


@user_vs.action("change")
class UserUpdateView(UserFormMixin, UpdateView):
    pass


@user_vs.action("delete")
class UserDeleteView(DeleteView):
    pass


@user_vs.action("detail", item=True, tab=True)
class UserDetailView(DetailView):
    detail_fields = UserFormMixin.fields


@group_vs.action("list")
class GroupListView(TableListView):
    list_display = ["name"]


@group_vs.action("add")
class GroupCreateView(CreateView):
    fields = ["name"]


@group_vs.action("change")
class GroupUpdateView(UpdateView):
    fields = ["name"]


@group_vs.action("delete")
class GroupDeleteView(DeleteView):
    pass


@group_vs.action("detail")
class GroupDetailView(DetailView):
    pass
