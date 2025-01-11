from formtools.wizard.views import SessionWizardView as BaseSessionWizardView

from .mixins import ViewSetMixin


class SessionWizardView(ViewSetMixin, BaseSessionWizardView):
    pass
