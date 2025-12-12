from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify


class DashboardWidget:
    order = 99
    view = None

    @property
    def name(self):
        return slugify(f"{self.__class__.__module__}-{self.__class__.__name__}")

    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)

    def __str__(self):
        return self.render()

    def get_context_data(self, **kwargs):
        return {}

    def render(self):
        context = self.get_context_data()
        return mark_safe(
            render_to_string(self.template_name, context, request=self.request)
        )

    def get_json_data(self):
        return {}
