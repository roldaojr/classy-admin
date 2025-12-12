from crispy_forms.helper import FormHelper
from django.contrib import messages
from django.db.models.base import ModelBase

from ..views.responses import TemplateBlockResponse
from ..viewsets.actions import Action
from ..viewsets.base import ViewSet
from .aaa import LoginRequiredMixin, PermissionRequiredMixin

__all__ = ("LoginRequiredMixin", "PermissionRequiredMixin")


class TemplateMixin:
    response_class = TemplateBlockResponse
    default_template_block = "content"

    def render_to_response(self, context, **response_kwargs):
        response: TemplateBlockResponse = super().render_to_response(
            context, **response_kwargs
        )
        response.template_block = self.default_template_block
        return response

    def get_template_names(self):
        templates_names = super().get_template_names()
        suffix = getattr(self, "template_name_suffix", None)
        if suffix:
            if suffix[0] == "_":
                suffix = suffix[1:]
            if self.action.modal:
                templates_names.append(f"modal/{suffix}.html")
            templates_names.append(f"{suffix}.html")
        return templates_names


class SuccessMessageMixin:
    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        instance = getattr(form, "instance", None) or getattr(self, "object", None)
        success_message = self.get_success_message(form.cleaned_data, instance)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data, instance):
        if self.success_message:
            return self.success_message.format(
                name=self.model._meta.verbose_name.title(),
                data=cleaned_data,
                obj=instance,
            )


class FormHelperMixin(SuccessMessageMixin):
    def get_form_helper(self):
        helper = FormHelper()
        helper.form_id = getattr(self, "form_id", None)
        helper.form_tag = False
        return helper

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not hasattr(form, "helper"):
            form.helper = self.get_form_helper()
        if hasattr(form, "layout"):
            form.helper.layout = form.layout() if callable(form.layout) else form.layout
        return form


class PageTitleMixin:
    def get_page_title(self):
        if self.page_title:
            return self.page_title
        if self.model:
            if self.action.default and not self.action.item:
                return self.model._meta.verbose_name_plural
            else:
                return " ".join(
                    [
                        self.action.verbose_name.capitalize(),
                        str(self.model._meta.verbose_name).capitalize(),
                    ]
                )
        return self.action.verbose_name.capitalize()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs, page_title=self.get_page_title())


class ViewSetMixin(
    PageTitleMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    SuccessMessageMixin,
    TemplateMixin,
):
    action: Action
    model: ModelBase
    viewset: ViewSet
    page_title = None
