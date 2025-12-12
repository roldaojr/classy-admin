from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import (
    PermissionRequiredMixin as DjangoPermissionRequiredMixin,
)
from django.core.exceptions import ImproperlyConfigured

from ..viewsets.actions import Action

__all__ = ["LoginRequiredMixin", "PermissionRequiredMixin"]


class PermissionRequiredMixin(DjangoPermissionRequiredMixin):
    action: Action

    def has_permission(self):
        if self.action.check:
            obj = None
            if self.action.item and hasattr(self, "get_object"):
                obj = self.get_object()
            return self.action.check(self.action, self.request, obj)
        return super().has_permission()

    def get_permission_required(self):
        if self.permission_required is not None:
            return super().get_permission_required()
        elif getattr(self, "action", None) and getattr(self, "model", None):
            perms = [
                "{}.{}_{}".format(
                    self.model._meta.app_label,
                    getattr(self.action, "perm", None) or getattr(self.action, "name"),
                    self.model._meta.model_name,
                ),
            ]
            self.permission_required = perms
            return self.permission_required

        raise ImproperlyConfigured(
            f"{self.__class__.__name__} is missing the "
            f"permission_required attribute. Define "
            f"{self.__class__.__name__}.permission_required, or override "
            f"{self.__class__.__name__}.get_permission_required()."
        )
