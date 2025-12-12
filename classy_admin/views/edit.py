from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic.edit import CreateView as DjangoCreateView
from django.views.generic.edit import DeleteView as DjangoDeleteView
from django.views.generic.edit import FormView as DjangoFormView
from django.views.generic.edit import UpdateView as DjangoUpdateView

from .log import ActionLogMixin
from .mixins import FormHelperMixin, ViewSetMixin


class CreateView(ActionLogMixin, FormHelperMixin, ViewSetMixin, DjangoCreateView):
    success_message = '{name} "{obj}" foi adicionado com êxito.'


class UpdateView(ActionLogMixin, FormHelperMixin, ViewSetMixin, DjangoUpdateView):
    success_message = '{name} "{obj}" foi atualizado com êxito.'


class DeleteView(ActionLogMixin, ViewSetMixin, DjangoDeleteView):
    delete_message = (
        "Tem certeza que excluir o {object._meta.verbose_name} <b>{object}</b>?"
    )
    success_message = '{name} "{obj}" foi deletado com êxito.'

    def get_delete_message(self, **kwargs) -> tuple[str, bool]:
        obj = getattr(self, "object", None)
        return self.delete_message.format(object=obj, **kwargs), True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Excluir {self.object._meta.verbose_name}"
        delete_message, can_delete = self.get_delete_message()
        context["delete_message"] = delete_message
        context["delete_disabled"] = not can_delete
        return context

    def form_valid(self, form):
        delete_message, can_delete = self.get_delete_message()
        if not can_delete:
            messages.warning(self.request, delete_message)
            return redirect(self.get_success_url())
        return super().form_valid(form)


class FormView(ActionLogMixin, ViewSetMixin, DjangoFormView):
    template_name_suffix = "_form"
