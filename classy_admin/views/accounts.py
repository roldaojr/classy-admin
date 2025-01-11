from django.contrib.auth.views import (
    LoginView as DjangoLoginView,
    LogoutView as DjangoLogoutView,
    PasswordChangeView as DjangoPasswordChangeView,
    PasswordResetView as DjangoPasswordResetView,
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
    PasswordResetDoneView as DjangoPasswordResetDoneView,
)
from django.utils.translation import gettext as _
from .mixins import TemplateMixin, PageTitleMixin
from ..viewsets.accounts import accounts_vs


@accounts_vs.action("login")
class LoginView(PageTitleMixin, TemplateMixin, DjangoLoginView):
    template_name = "classy_admin/accounts/login.html"
    page_title = _("Log in")


@accounts_vs.action("logout")
class LogoutView(PageTitleMixin, TemplateMixin, DjangoLogoutView):
    http_method_names = ["get", "post", "options"]
    page_title = _("Log out")

    def get_template_names(self):
        if self.request.method == "post":
            return "classy_admin/accounts/logged_out.html"
        return "classy_admin/accounts/logout.html"


@accounts_vs.action("password_change")
class PasswordChangeView(PageTitleMixin, TemplateMixin, DjangoPasswordChangeView):
    template_name = "classy_admin/accounts/password_change_form.html"
    page_title = DjangoPasswordChangeView.title


@accounts_vs.action("password_reset")
class PasswordResetView(PageTitleMixin, TemplateMixin, DjangoPasswordResetView):
    template_name = "classy_admin/accounts/password_reset_form.html"
    page_title = DjangoPasswordResetView.title


@accounts_vs.action("password_reset_confirm")
class PasswordResetConfirmView(
    PageTitleMixin, TemplateMixin, DjangoPasswordResetConfirmView
):
    template_name = "classy_admin/accounts/password_reset_confirm.html"
    page_title = DjangoPasswordResetConfirmView.title


@accounts_vs.action("password_reset_done")
class PasswordResetDoneView(PageTitleMixin, TemplateMixin, DjangoPasswordResetDoneView):
    template_name = "classy_admin/accounts/password_reset_done.html"
    page_title = DjangoPasswordResetDoneView.title
