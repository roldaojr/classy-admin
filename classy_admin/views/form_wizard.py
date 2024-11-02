from formtools.wizard.views import SessionWizardView as BaseSessionWizardView
from .mixins import AdminMixin


class SessionWizardView(AdminMixin, BaseSessionWizardView):
    pass
