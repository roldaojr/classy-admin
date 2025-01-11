from typing import TYPE_CHECKING

from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext as _
from django_tables2.columns import TemplateColumn

from .actions import Action, ActionsManager

if TYPE_CHECKING:
    from .base import ViewSet


class WithActionMixin:
    request: HttpRequest
    action: Action = None
    viewset: "ViewSet" = None
    model: ModelBase = None
    actions: ActionsManager = ActionsManager()

    @property
    def model_meta(self):
        return self.model._meta

    def get_table_kwargs(self):
        display_action_names = getattr(self.viewset, "display_action_names", None)
        extra_columns = []
        if getattr(self, "actions_column", True):
            extra_columns.append(
                (
                    "actions",
                    TemplateColumn(
                        extra_context={"actions_names": display_action_names},
                        template_name="classy_admin/list/_item_actions.html",
                        verbose_name=_("Actions"),
                        attrs={"cell": {"class": "text-end"}},
                    ),
                )
            )
        return {"extra_columns": extra_columns}

    def get_success_url(self):
        try:
            return super().get_success_url()
        except ImproperlyConfigured:
            default_action: Action = self.actions.non_item_default
            return reverse(default_action.url_name)
