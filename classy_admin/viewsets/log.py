from django.apps import apps

from .actions import Action

action_mapping = {"add": 1, "change": 2, "delete": 3}


class ActionLogMixin:
    action: Action
    enable_action_log = True

    def form_valid(self, *args, **kwargs):
        response = super().form_valid(*args, **kwargs)
        if self.enable_action_log:
            self.log_action()
        return response

    def log_action(self):
        target_obj = None
        if hasattr(self, "object"):
            target_obj = self.object
        elif self.request.user.is_authenticated:
            target_obj = self.request.user

        if target_obj is None:
            return  # disable log if has not object

        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.pk

        LogEntry = apps.get_model("admin", "LogEntry")
        LogEntry.objects.log_actions(
            user_id=user_id,
            queryset=[target_obj],
            action_flag=action_mapping.get(self.action.name, 2),
            change_message=self.action.verbose_name,
            single_object=True,
        )
