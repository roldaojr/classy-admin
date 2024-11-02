from extra_views.advanced import (
    BaseCreateWithInlinesView,
    BaseUpdateWithInlinesView,
    NamedFormsetsMixin,
)
from .edit import AdminMixin


class CreateWithInlinesView(AdminMixin, NamedFormsetsMixin, BaseCreateWithInlinesView):
    template_name_suffix = "_form"
    success_message = '{name} "{obj}" foi adicionado com êxito.'


class UpdateWithInlinesView(AdminMixin, NamedFormsetsMixin, BaseUpdateWithInlinesView):
    template_name_suffix = "_form"
    success_message = '{name} "{obj}" foi atualizado com êxito.'
