from extra_views.advanced import CreateWithInlinesView as BaseCreateWithInlinesView
from extra_views.advanced import NamedFormsetsMixin
from extra_views.advanced import UpdateWithInlinesView as BaseUpdateWithInlinesView

from .mixins import FormHelperMixin, ViewSetMixin


class CreateWithInlinesView(
    ViewSetMixin, NamedFormsetsMixin, FormHelperMixin, BaseCreateWithInlinesView
):
    success_message = '{name} "{obj}" foi adicionado com êxito.'


class UpdateWithInlinesView(
    ViewSetMixin, NamedFormsetsMixin, FormHelperMixin, BaseUpdateWithInlinesView
):
    success_message = '{name} "{obj}" foi atualizado com êxito.'
