from django.apps import apps
from django.db.models import Model

from ..viewsets.actions import Action

action_names_map = {"create": 1, "add": 1, "delete": 3}


class ActionLogMixin:
    action: Action

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_actions([self.object])
        return response

    def log_actions(self, instances: list[Model]):
        if not apps.is_installed("django.contrib.admin"):
            # do not log if django admin ont installed
            return
        if not self.request.user.is_authenticated:
            # do not log anonymous user action
            return
        LogEntry = apps.get_model("admin.LogEntry")
        LogEntry.objects.log_actions(
            self.request.user.pk,
            instances,
            action_names_map.get(self.action.name, 2),
            single_object=True,
        )
