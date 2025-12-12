from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _
from simple_menu import Menu, MenuItem

from .registries import viewset_registry

if getattr(settings, "CLASSY_ADMIN_MENU", True):
    viewset_registry.add_menu_items()

if getattr(settings, "CLASSY_ADMIN_USER_MENU", True):
    user_menu_items = [
        MenuItem(
            _("Change password"),
            url=reverse("classy_admin:accounts-password_change"),
        ),
        MenuItem("", "", separator=True),
        MenuItem(_("Log out"), url=reverse("classy_admin:accounts-logout"), modal=True),
    ]
    for item in user_menu_items:
        Menu.add_item("user_menu", item)
