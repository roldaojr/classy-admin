from collections import OrderedDict
from collections.abc import Callable

from django.db.models.base import ModelBase
from django.urls import include, path, reverse
from django.urls.resolvers import URLPattern
from django.views.generic import View
from simple_menu import MenuItem

from ..registries import viewset_registry
from .actions import ACTIONS_TEMPLATES, Action
from .mixins import WithActionMixin


class ViewSet:
    _actions: dict[str, Action]
    model: ModelBase = None
    name: str = None
    url_prefix: str = None

    def __init__(
        self,
        model: ModelBase = None,
        name: str = None,
        register: bool = True,
        **kwargs,
    ) -> None:
        self._actions = {}

        if model is not None:
            self.model = model
            self.model_name = self.model._meta.model_name
            self.app_label = self.model._meta.app_label
            if name is None:
                name = f"{self.app_label}-{self.model_name}"

        if name is not None:
            self.name = name

        if register:
            viewset_registry.register(self)

        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __repr__(self) -> str:
        self_type = type(self).__name__
        return f"<{self_type} name='{self.name}'>"

    def action(
        self,
        name: str,
        *,
        verbose_name: str = None,
        item: bool = None,
        batch: bool = None,
        default: bool = None,
        hidden: bool = None,
        tab: bool = None,
        url_path: str = None,
        perm: str = None,
        icon: str = None,
        check: Callable = None,
        **kwargs,
    ):
        """Add action to viewset

        Arguments:
                name (str): Name of the action
        Keyword arguments:
                verbose_name (str): Name to show in pages
                item (bool): action on the model instance
                batch (bool): action on a set of model instances
                default (bool): Is the default action
                hidden (bool): Action will not show in user interface
                tab (bool): Action will show in tab interface
                url_path (str): URL path
                perm (str): Permission required to execute the action
                icon (str): Icon to show in the button and menus
                check (callable): callable to check is visible
        """
        kwargs.update(
            dict(
                verbose_name=verbose_name,
                item=item,
                batch=batch,
                default=default,
                hidden=hidden,
                tab=tab,
                url_path=url_path,
                perm=perm,
                icon=icon,
                check=check,
                viewset=self,
            )
        )
        self._update_action_kwargs(name, kwargs)

        def decorator(view_class: type[View]):
            self._actions[name] = Action(
                **kwargs,
                name=name,
                view_class=view_with_action(view_class),
            )
            return view_class

        return decorator

    def _update_action_kwargs(
        self,
        name: str,
        kwargs: dict,
        actions_templates: dict[str, dict] = ACTIONS_TEMPLATES,
    ) -> None:
        # replace None values with action template values
        default_template = actions_templates.get(None) or {}
        action_template = actions_templates.get(name, default_template)
        for template in [action_template, default_template]:
            for attr, val in template.items():
                if kwargs.get(attr, None) is None:
                    kwargs[attr] = val
        # if has not verbose_name use action name
        if not kwargs.get("verbose_name"):
            kwargs["verbose_name"] = name
        # upper case verbose name
        kwargs["verbose_name"] = kwargs.get("verbose_name", name).capitalize()

    def get_view_kwargs(self, action):
        kwargs = {"viewset": self, "action": action}
        if self.model is not None:
            kwargs["model"] = self.model
        return kwargs

    def _urlpatterns(self, namespace: str = None) -> list[URLPattern]:
        self.namespace = namespace
        patterns = []
        actions: list = sorted(
            self._actions.items(), key=lambda i: int(i[1].item or False)
        )
        for name, action in actions:
            url_path = []
            if action.url_path:
                url_path.append(action.url_path)
            else:
                if action.item:
                    url_path.append("<str:pk>")
                if not action.default:
                    url_path.append(name)

            view_kwargs = self.get_view_kwargs(action)

            patterns.append(
                path(
                    "/".join(url_path),
                    action.view_class.as_view(**view_kwargs),
                    name=action.get_url_name(),
                )
            )
        return patterns

    def get_menu_item(self, namespace: str = None) -> MenuItem:
        """Get default action menu item"""
        default_actions = [
            a for _, a in self._actions.items() if a.default and not a.item
        ]
        default_action = default_actions[0]
        default_url = reverse(default_action.url_name)
        if default_url:
            title = (
                self.model._meta.verbose_name_plural.title()
                if self.model
                else self.name
            )
            return MenuItem(
                title,
                url=default_url,
                icon=default_action.icon,
                weight=default_action.order or 10,
            )

    def get_url_path(self, namespace=None):
        if self.model:
            prefix = f"{self.app_label}/{self.model_name}/"
        elif self.name:
            prefix = f"{self.name}/"
        return path(prefix, include(self._urlpatterns(namespace=namespace)))

    @property
    def bound_actions(self) -> dict[str, Action]:
        return OrderedDict(
            sorted(self._actions.items(), key=lambda i: i[1].order or 99)
        )


def view_with_action(view_class):
    if WithActionMixin not in view_class.__mro__:
        view_class = type(
            f"{view_class.__module__}.{view_class.__name__}Action",
            (WithActionMixin, view_class),
            {},
        )
    return view_class
