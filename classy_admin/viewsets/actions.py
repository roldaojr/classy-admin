from collections.abc import Callable
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, Self

from django.core.exceptions import ImproperlyConfigured
from django.db.models.options import Options
from django.http import HttpRequest, HttpResponse

if TYPE_CHECKING:
    from .base import ViewSet
    from .mixins import WithActionMixin

# basic actions attributes
ACTIONS_TEMPLATES: dict[dict] = {
    "list": dict(
        item=False,
        default=True,
        verbose_name="listar",
        perm="view",
    ),
    "add": dict(
        item=False,
        default=False,
        verbose_name="cadastrar",
        perm="add",
    ),
    "change": dict(
        item=True,
        default=False,
        verbose_name="editar",
        icon="ki-outline ki-notepad-edit",
        perm="change",
        order=51,
    ),
    "detail": dict(
        item=True,
        default=True,
        verbose_name="ver",
        icon="ki-outline ki-eye",
        perm="view",
        order=1,
    ),
    "delete": dict(
        item=True,
        default=False,
        modal=True,
        verbose_name="excluir",
        icon="ki-outline ki-trash",
        perm="delete",
        css_class="btn-light-danger",
        order=100,
    ),
    None: dict(
        item=False,
        batch=False,
        default=False,
        hidden=False,
        tab=False,
        css_class="btn-light-info",
        order=99,
    ),
}

# action aliases
ACTIONS_TEMPLATES.update({"edit": ACTIONS_TEMPLATES["change"]})


class Action(SimpleNamespace):
    """
    Represents an action within a viewset with configurable properties and permissions.

    This class defines the structure and behavior of actions that can be performed
    in an administrative or management interface, with support for item-level and
    bulk operations, permissions, and dynamic URL generation.

    Attributes:
        name (str): Unique identifier for the action.
        verbose_name (str, optional): Human-readable name for the action.
        item (bool): Whether the action applies to individual items.
        bulk (bool): Whether the action can be applied to multiple items.
        default (bool): Indicates if this is the default action.
        hidden (bool): Determines if the action should be hidden from user interface.
        tab (bool): Determines if the action displayed in tab interface.
        modal (bool): Whether the action should be displayed in a modal.
        url_path (str, optional): Custom URL path for the action.
        perm (str, optional): Permission required to perform the action.
        icon (str, optional): Icon identifier for the action.
        order (int, optional): Sorting order for the action.
        check (Callable): Function to determine if the action is visible.
    """

    name: str
    verbose_name: str = None
    item: bool = False
    bulk: bool = False
    default: bool = False
    hidden: bool = False
    tab: bool = False
    modal: bool = False
    url_path: str = None
    perm: str = None
    icon: str = None
    order: int = None
    check: Callable[[Self, HttpRequest, Any | None], bool]
    url: str
    view_class: type["WithActionMixin"]
    view: Callable[[HttpRequest], HttpResponse]
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
        perm = self.perm or self.name
        if self.viewset.model:
            meta: Options = self.viewset.model._meta
            return f"{meta.app_label}.{perm}_{meta.model_name}"
        return f"{perm}_{self.viewset.name}"

    @staticmethod
    def check(action: "Action", request: HttpRequest, obj=None) -> bool:
        if action.perm is None:
            return True
        return request.user.has_perm(action.perm_name, obj)

    def __str__(self) -> str:
        return self.name

    def get_url_name(self) -> str:
        if self.viewset.name:
            return f"{self.viewset.name}-{self.name}"
        return self.name


class ActionsManager:
    view: "WithActionMixin"

    @property
    def viewset(self) -> "ViewSet":
        return self.view.viewset

    @property
    def request(self):
        return self.view.request

    def __get__(self, obj, obj_type=None) -> dict[str, Action]:
        self.view = obj
        return self

    def __set_name__(self, view, name):
        self.view = view
        self.__name__ = name

    def __set__(self):
        raise AttributeError(f"{self.attr_name} attribute can not be changed")

    def __repr__(self):
        return f"<{self.__class__.__name__} of {self.viewset.__class__.__name__}({self.viewset.name})>"

    def registered(self) -> dict[str, Action]:
        return self.viewset.bound_actions

    def _allowed(self, include_hidden=False, **kwargs) -> dict[str, Action]:
        actions = {}
        for name, action in self.registered().items():
            if action.hidden and not include_hidden:
                continue
            if self.view and self.view.action.name == name:
                continue
            if not all(
                [getattr(action, attr, False) == val for attr, val in kwargs.items()]
            ):
                continue
            if action.check is not None and not action.check(action, self.request):
                continue
            if action.perm and not self.request.user.has_perm(action.perm_name):
                continue
            actions[name] = action
        return actions

    def _only_default(self, actions: dict[str, Action]) -> Action:
        default_actions = [a for _, a in actions.items() if a.default]
        if not default_actions:
            return None
        if len(default_actions) != 1:
            raise ImproperlyConfigured(
                f"Must be one default action available. Defined: {default_actions}"
            )
        return default_actions[0]

    @property
    def allowed(self) -> dict[str, Action]:
        return self._allowed(include_hidden=True)

    @property
    def non_item(self) -> dict[str, Action]:
        return self._allowed(item=False)

    @property
    def item(self) -> dict[str, Action]:
        return self._allowed(item=True)

    @property
    def bulk(self) -> dict[str, Action]:
        return self._allowed(bulk=True)

    @property
    def tab(self) -> dict[str, Action]:
        return self._allowed(tab=True)

    @property
    def tab_item(self) -> dict[str, Action]:
        return self._allowed(item=True, tab=True)

    @property
    def non_item_default(self) -> Action:
        return self._only_default(self.non_item)

    @property
    def item_default(self) -> Action:
        return self._only_default(self.item)

    @property
    def tab_default(self) -> Action:
        return self._only_default(self.tab)

    @property
    def tab_item_default(self) -> Action:
        return self._only_default(self.tab_item)


class ChildrenActionsManager(ActionsManager):
    @property
    def viewset(self) -> "ViewSet":
        return self._viewset

    @property
    def request(self):
        return self._request

    def __init__(self, viewset: "ViewSet", request: HttpRequest):
        self._viewset = viewset
        self._request = request
        self.view = None
