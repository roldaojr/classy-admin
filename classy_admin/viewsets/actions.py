from types import SimpleNamespace
from typing import Callable, Self, TYPE_CHECKING, Type
from functools import partialmethod, partial

from django_tables2.columns import TemplateColumn
from django.views.generic import View
from django.db.models.options import Options
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.generic import View

if TYPE_CHECKING:
    from .base import ViewSet
    from .mixins import WithActionMixin

# basic actions attributes
ACTIONS_TEMPLATES: dict[dict] = {
    "list": dict(
        item=False,
        default=True,
        verbose_name=_("list"),
        perm="view",
    ),
    "add": dict(
        item=False,
        default=False,
        verbose_name=_("add"),
        icon="fas fa-plus",
        perm="add",
    ),
    "change": dict(
        item=True,
        default=False,
        verbose_name=_("change"),
        icon="fas fa-pencil",
        order=51,
    ),
    "detail": dict(
        item=True,
        default=True,
        verbose_name=_("detail"),
        icon="fas fa-eye",
        order=1,
    ),
    "delete": dict(
        item=True,
        default=False,
        verbose_name=_("delete"),
        icon="fas fa-trash",
        order=100,
    ),
}

# action aliases
ACTIONS_TEMPLATES.update({"edit": ACTIONS_TEMPLATES["change"]})


class Action(SimpleNamespace):
    """Action class"""

    name: str
    verbose_name: str = None
    item: bool = False
    bulk: bool = False
    default: bool = False
    hidden: bool = False
    url_path: str = None
    perm: str = None
    icon: str = None
    order: int = None
    check: Callable[[Self, HttpRequest], bool]
    url: str
    view_class: View
    view: "WithActionMixin" | Callable[[HttpRequest], HttpResponse]
    viewset: "ViewSet"

    @property
    def url_name(self) -> str:
        names = []
        if self.viewset.namespace:
            names.append(self.viewset.namespace)
        names.append(self.get_url_name())
        return ":".join(names)

    @property
    def perm_name(self):
        perm = [self.perm or self.name]
        if self.viewset.model:
            meta: Options = self.viewset.model._meta
            perm + [meta.app_label, meta.model_name]
        if self.perm:
            perm.append(self.name)
        return "_".join(perm)

    @staticmethod
    def check(action: "Action", request: HttpRequest) -> bool:
        return request.user.has_perm(action.perm_name)

    def __str__(self) -> str:
        return self.name

    def get_url_name(self) -> str:
        if self.viewset.name:
            return f"{self.viewset.name}-{self.name}"
        return self.name


class ActionsManager:
    def __init__(self, viewset: "ViewSet", request: HttpRequest) -> None:
        self.viewset = viewset
        self.request = request

    def all(self) -> dict[str, Action]:
        return self.viewset.bound_actions

    def _default(self, method: partialmethod) -> Action:
        get_actions: Callable[[], dict[str, Action]] = method.__get__(self)
        default_actions = [a for _, a in get_actions().items() if a.default]
        if len(default_actions) != 1:
            raise ImproperlyConfigured("Must be only default action available")
        return default_actions[0]

    def allowed(self, **kwargs) -> dict[str, Action]:
        actions = {}
        for name, action in self.all().items():
            for attr, val in kwargs.items():
                attr_val = getattr(action, attr, None)
                if attr_val == val and (
                    action.check is None or action.check(self, self.request)
                ):
                    actions[name] = action
        return actions

    def __get__(self) -> dict[str, Action]:
        return self.allowed()

    list = partialmethod(allowed, item=False, bulk=False, tab=False)
    item = partialmethod(allowed, item=True)
    bulk = partialmethod(allowed, bulk=True)
    tab = partialmethod(allowed, tab=True)
    tab_item = partialmethod(allowed, item=True, tab=True)
    list_default = partialmethod(_default, list)
    item_default = partialmethod(_default, item)
    tab_default = partialmethod(_default, tab)
    tab_item_default = partialmethod(_default, tab_item)
