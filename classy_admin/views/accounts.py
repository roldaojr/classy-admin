from django.contrib import messages
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from django.contrib.auth.views import (
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
)
from django.contrib.auth.views import (
    PasswordResetDoneView as DjangoPasswordResetDoneView,
)
from django.contrib.auth.views import PasswordResetView as DjangoPasswordResetView
from django.urls import reverse
from django.utils.translation import gettext as _

from ..viewsets.accounts import accounts_vs
from .mixins import PageTitleMixin, TemplateMixin


@accounts_vs.action("login")
class LoginView(PageTitleMixin, TemplateMixin, DjangoLoginView):
    template_name = "accounts/login.html"
    page_title = _("Log in")


@accounts_vs.action("logout")
class LogoutView(PageTitleMixin, TemplateMixin, DjangoLogoutView):
    http_method_names = ["get", "post", "options"]
    page_title = _("Log out")

    def get_template_names(self):
        if not self.request.user.is_authenticated:
            return "accounts/logged_out.html"
        return "accounts/logout.html"


@accounts_vs.action("password_change")
class PasswordChangeView(PageTitleMixin, TemplateMixin, DjangoPasswordChangeView):
    template_name = "accounts/password_change_form.html"
    page_title = DjangoPasswordChangeView.title


@accounts_vs.action("password_reset")
class PasswordResetView(PageTitleMixin, TemplateMixin, DjangoPasswordResetView):
    template_name = "accounts/password_reset_form.html"
    page_title = DjangoPasswordResetView.title
    subject_template_name = "registration/password_reset_subject.txt"
    email_template_name = "accounts/password_reset_email.html"
    from_email = None
    html_email_template_name = None

    @property
    def extra_email_context(self):
        return {
            "password_reset_confirm_url_name": f"{self.viewset.namespace}:{self.viewset.name}-password_reset_confirm"
        }

    def get_success_url(self):
        return reverse(
            f"{self.viewset.namespace}:{self.viewset.name}-password_reset_done"
        )


@accounts_vs.action(
    "password_reset_confirm", url_path="password_reset_confirm/<uidb64>/<token>/"
)
class PasswordResetConfirmView(
    PageTitleMixin, TemplateMixin, DjangoPasswordResetConfirmView
):
    template_name = "accounts/password_reset_confirm.html"
    page_title = DjangoPasswordResetConfirmView.title

    def get_success_url(self):
        messages.success(
            self.request,
            _("Your password has been set.  You may go ahead and log in now."),
        )
        return reverse(f"{self.viewset.namespace}:{self.viewset.name}-login")


@accounts_vs.action("password_reset_done")
class PasswordResetDoneView(PageTitleMixin, TemplateMixin, DjangoPasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"
    page_title = DjangoPasswordResetDoneView.title
