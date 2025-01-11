from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class DashboardWidget:
    order = 99

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def get_context_data(self, **kwargs):
        return {}

    def render(self):
        context = self.get_context_data()
        return mark_safe(
            render_to_string(self.template_name, context, request=self.request)
        )

    def __str__(self):
        return self.render()
