from types import SimpleNamespace

from django.urls import reverse
from django.utils.translation import gettext as _


class Breadcrumb(SimpleNamespace):
    title: str
    url: str

    def __str__(self):
        return self.title


class BreadcrumbsMixin:
    def get_breadcrumbs(self):
        """
        Returns the breadcrumbs for the viewset.
        """
        breadcrumbs = []
        if getattr(self, "model", None):
            # breadcrumbs.append(apps.get_app_config(self.model._meta.app_label).verbose_name)
            breadcrumbs.append(
                Breadcrumb(title=self.model._meta.verbose_name_plural.title())
            )  # NOQA
            default_action = self.actions.non_item_default
            if default_action:
                breadcrumbs[-1].url = reverse(default_action.url_name)
            if self.action:
                if self.action.item or not self.action.default:
                    action_title = self.action.verbose_name or self.action.name
                    breadcrumbs.append(Breadcrumb(title=_(action_title).capitalize()))
                if self.action.item and self.action.default and self.object:
                    breadcrumbs[-1].title += f" {self.object}"
        return breadcrumbs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["breadcrumbs"] = self.get_breadcrumbs()
        return context
