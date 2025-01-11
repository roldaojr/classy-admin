from extra_views.advanced import (
    BaseCreateWithInlinesView,
    BaseUpdateWithInlinesView,
    NamedFormsetsMixin,
)

from .edit import ViewSetMixin


class CreateWithInlinesView(
    ViewSetMixin, NamedFormsetsMixin, BaseCreateWithInlinesView
):
    template_name_suffix = "_form"
    success_message = '{name} "{obj}" foi adicionado com êxito.'


class UpdateWithInlinesView(
    ViewSetMixin, NamedFormsetsMixin, BaseUpdateWithInlinesView
):
    template_name_suffix = "_form"
    success_message = '{name} "{obj}" foi atualizado com êxito.'
