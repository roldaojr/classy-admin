from django_select2.forms import (
    ModelSelect2MultipleWidget as DjangoModelSelect2MultipleWidget,
)
from django_select2.forms import ModelSelect2Widget as DjangoModelSelect2Widget
from django_select2.forms import Select2MultipleWidget as DjangoSelect2MultipleWidget
from django_select2.forms import Select2Widget as DjangoSelect2Widget


class Select2Mixin:
    empty_label = "Selecionar"

    def build_attrs(self, base_attrs, extra_attrs=None):
        if extra_attrs is None:
            extra_attrs = {}
        extra_attrs.update({"data-minimum-input-length": 0})
        return super().build_attrs(base_attrs, extra_attrs)


class ModelSelect2Widget(Select2Mixin, DjangoModelSelect2Widget):
    pass


class ModelSelect2MultipleWidget(Select2Mixin, DjangoModelSelect2MultipleWidget):
    pass


class Select2Widget(Select2Mixin, DjangoSelect2Widget):
    pass


class Select2MultipleWidget(DjangoSelect2MultipleWidget):
    pass
