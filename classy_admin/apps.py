from django.apps import AppConfig, apps

from .registries import dashboard_registry, viewset_registry


class ClassyAdminConfig(AppConfig):
    name = "classy_admin"

    def ready(self):
        super().ready()
        app_names = [app.name for app in apps.app_configs.values()]
        # discover viewsets
        viewset_registry.autodiscover(app_names)
        # discover dashboard widgets
        dashboard_registry.autodiscover(app_names)
