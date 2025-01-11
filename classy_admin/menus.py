from django.conf import settings
from django.utils.translation import gettext as _
from django.urls import reverse
from simple_menu import Menu, MenuItem
from .registries import viewset_registry

if getattr(settings, "CLASSY_ADMIN_MENU", True):
    viewset_registry.add_menu_items()

if getattr(settings, "CLASSY_ADMIN_USER_MENU", True):
    Menu.add_item(
        "user_menu",
        MenuItem(
            _("Change password"),
            url="",  # reverse("classy_admin:accounts-passwordchange")
        ),
    )
    Menu.add_item(
        "user_menu",
        MenuItem(_("Log out"), url=reverse("classy_admin:accounts-logout")),
    )
