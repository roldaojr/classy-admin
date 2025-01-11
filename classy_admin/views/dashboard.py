from django.views.generic import TemplateView

from ..registries import dashboard_registry
from ..viewsets.home import default_vs
from .mixins import ViewSetMixin


@default_vs.action("dashboard", default=True)
class DashboardView(ViewSetMixin, TemplateView):
    template_name = "classy_admin/dashboard.html"
    permission_required = []

    def get_page_title(self):
        return "Dashboard"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        registered_widgets = sorted(dashboard_registry.values(), key=lambda i: i.order)
        context["widgets"] = [
            widget_class(self.request) for widget_class in registered_widgets
        ]
        return context
