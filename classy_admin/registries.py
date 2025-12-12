import typing
from collections import defaultdict

from django.apps import apps
from django.conf import settings
from django.urls import include, path
from persisting_theory import Registry
from simple_menu import Menu, MenuItem

if typing.TYPE_CHECKING:
    from .viewsets.base import ViewSet


class ViewSetRegistry(Registry):
    look_into = "views"
    namespace = "classy_admin"
    default_viewset: "ViewSet"

    @property
    def urls(self):
        """URLs from registred viewsets with default namespace"""
        return self.get_urls()

    def get_urls(self, namespace=None):
        """URLs from registred viewsets with specified namespace"""
        if not namespace:
            namespace = self.namespace
        viewsets: list[ViewSet] = self.values()
        return (
            [
                vs.get_url_path(namespace=namespace)
                for vs in viewsets
                if vs != self.default_viewset
            ]
            + [
                path(
                    "",
                    include(
                        self.default_viewset._urlpatterns(namespace=self.namespace)
                    ),
                )
            ],
            "viewsets",
            namespace,
        )

    def add_menu_items(self, menu_name: str | None = None):
        vs: ViewSet
        app_menu_items = defaultdict(list)
        if not menu_name:
            menu_name = self.namespace
        menu_groups = getattr(settings, "MENU_APP_GROUPS", True)

        for vs in self.values():
            # add menu items from viewsets
            app_label = vs.model._meta.app_label if vs.model and menu_groups else None
            subitem = vs.get_menu_item(self.namespace)
            if subitem:
                app_menu_items[app_label].append(subitem)

        for app_label, subitems in app_menu_items.items():
            # add menu items to root menu
            if len(subitems) == 0:
                continue
            if app_label:
                app = apps.get_app_config(app_label)
                app_icon = getattr(app, "menu_icon", None)
                item = MenuItem(
                    app.verbose_name,
                    url="#",
                    icon=app_icon,
                    children=subitems,
                )
                Menu.add_item(menu_name, item)
            else:
                # if not app_label, add items to root menu
                for item in subitems:
                    Menu.add_item(menu_name, item)

    def autodiscover(self, force_reload=False):
        app_names = [
            app_config.name
            for app_config in apps.get_app_configs()
            if app_config.name != "classy_admin"
        ]
        return super().autodiscover(app_names, force_reload)

    def get_object_name(self, data):
        if hasattr(data, "name"):
            return data.name
        return super().get_object_name(data)


class DashboardWidgetRegistry(Registry):
    look_into = "dashboard_widgets"

    def prepare_name(self, data, name=None):
        if name is not None:
            return name
        if hasattr(data, "name"):
            name = data.name
        name = self.get_object_name(data)
        module = getattr(data, "__module__", None)
        if module is not None:
            return f"{module}.{name}"
        return name


viewset_registry = ViewSetRegistry()
dashboard_registry = DashboardWidgetRegistry()
