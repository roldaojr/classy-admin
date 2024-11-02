from django.views.generic.edit import (
    CreateView as DjangoCreateView,
    DeleteView as DjangoDeleteView,
    FormView as DjangoFormView,
    UpdateView as DjangoUpdateView,
)

from .aaa import LoginRequiredMixin, PermissionRequiredMixin
from .mixins import TemplateMixin, AdminMixin, FormHelperMixin


class CreateView(FormHelperMixin, AdminMixin, DjangoCreateView):
    success_message = '{name} "{obj}" foi adicionado com êxito.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Adicionar {self.model._meta.verbose_name}"
        return context


class UpdateView(FormHelperMixin, AdminMixin, DjangoUpdateView):
    success_message = '{name} "{obj}" foi atualizado com êxito.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Alterar {self.model._meta.verbose_name}"
        return context


class DeleteView(AdminMixin, DjangoDeleteView):
    delete_message = (
        "Deseja realmente exluir o {object._meta.verbose_name} <b>{object}</b>?"
    )
    success_message = '{name} "{obj}" foi deletado com êxito.'

    def get_delete_message(self, **kwargs):
        obj = getattr(self, "object", None)
        return self.delete_message.format(object=obj, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Apagar {self.object._meta.verbose_name}"
        context["delete_message"] = self.get_delete_message()
        return context


class FormView(AdminMixin, DjangoFormView):
    template_name_suffix = "_form"
