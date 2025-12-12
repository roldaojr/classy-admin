from typing import TYPE_CHECKING

from django.core.exceptions import ImproperlyConfigured
from django.db.models.base import ModelBase
from django.http import HttpRequest
from django.urls import reverse
from django_tables2.columns import Column, TemplateColumn

from .actions import Action, ActionsManager
from .breadcrumbs import BreadcrumbsMixin
from .log import ActionLogMixin

if TYPE_CHECKING:
    from .base import ViewSet


class TableListMixin:
    table_extra_columns: list[tuple[str, Column]] = []
    actions_column = True

    def get_table_kwargs(self):
        display_action_icons = getattr(self.viewset, "display_action_icons", None)
        display_action_labels = getattr(self.viewset, "display_action_labels", None)
        extra_columns = self.table_extra_columns.copy()
        if self.actions_column:
            extra_columns.append(
                (
                    "actions",
                    TemplateColumn(
                        extra_context={
                            "action_icons": display_action_icons,
                            "action_labels": display_action_labels,
                        },
                        template_name="list/_item_actions.html",
                        verbose_name="Ações",
                        orderable=False,
                        attrs={"cell": {"class": "text-end list-actions"}},
                    ),
                )
            )
        return {"extra_columns": extra_columns}


class SuccessUrlDefaultActionMixin:
    def get_success_url(self):
        if hasattr(super(), "get_success_url"):
            try:
                return super().get_success_url()
            except ImproperlyConfigured:
                pass
        default_action: Action = self.actions.non_item_default
        return reverse(default_action.url_name)


class WithActionMixin(
    TableListMixin, SuccessUrlDefaultActionMixin, ActionLogMixin, BreadcrumbsMixin
):
    request: HttpRequest
    action: Action = None
    viewset: "ViewSet" = None
    model: ModelBase = None
    actions: ActionsManager = ActionsManager()

    @property
    def model_meta(self):
        return self.model._meta
