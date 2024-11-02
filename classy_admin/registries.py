import typing
from itertools import groupby
from django.apps import apps
from django.urls import include, path
from persisting_theory import Registry
from simple_menu import Menu, MenuItem

if typing.TYPE_CHECKING:
    from .viewsets.base import ViewSet


class ViewSetRegistry(Registry):
    look_into = "views"
    namespace = "classy-admin"

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
            [vs.get_url_path(namespace=namespace) for vs in viewsets],
            "viewsets",
            namespace,
        )

    def add_menu_items(self, menu_name: str | None = None):
        for app_label, viewsets in groupby(
            self.values(), lambda vs: vs.model._meta.app_label
        ):
            app = apps.get_app_config(app_label)
            item = MenuItem(app.verbose_name, url="#", children=[])
            for vs in viewsets:
                vs: ViewSet
                subitem = vs.get_menu_item(self.namespace)
                if subitem:
                    item.children.append(subitem)
            Menu.add_item(menu_name or self.namespace, item)

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


viewset_registry = ViewSetRegistry()
