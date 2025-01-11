from django.views.generic.edit import CreateView as DjangoCreateView
from django.views.generic.edit import DeleteView as DjangoDeleteView
from django.views.generic.edit import FormView as DjangoFormView
from django.views.generic.edit import UpdateView as DjangoUpdateView

from .mixins import FormHelperMixin, ViewSetMixin


class CreateView(FormHelperMixin, ViewSetMixin, DjangoCreateView):
    success_message = '{name} "{obj}" foi adicionado com êxito.'


class UpdateView(FormHelperMixin, ViewSetMixin, DjangoUpdateView):
    success_message = '{name} "{obj}" foi atualizado com êxito.'


class DeleteView(ViewSetMixin, DjangoDeleteView):
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


class FormView(ViewSetMixin, DjangoFormView):
    template_name_suffix = "_form"
