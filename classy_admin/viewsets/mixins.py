from typing import TYPE_CHECKING
from django.db.models.base import ModelBase
from django.http import HttpRequest
from django.utils.functional import cached_property
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

    @cached_property
    def actions(self):
        return ActionsManager(self.viewset, self.request)

    @property
    def model_meta(self):
        return self.model._meta

    def get_table_kwargs(self):
        display_action_names = getattr(self.viewset, "display_action_names", None)
        return {
            "extra_columns": [
                (
                    "actions",
                    TemplateColumn(
                        extra_context={"actions_names": display_action_names},
                        template_name="classy_admin/list/_item_actions.html",
                        verbose_name=_("Actions"),
                    ),
                )
            ]
        }
