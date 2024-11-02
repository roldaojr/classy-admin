from collections import OrderedDict

from django.views.generic import DetailView as DjangoDetailView
from django.views.generic.detail import SingleObjectMixin
from django_tables2.utils import Accessor

from .aaa import LoginRequiredMixin, PermissionRequiredMixin
from .mixins import TemplateMixin


class DetailMixin(SingleObjectMixin):
    detail_fields = []
    object = None

    def get_details(self, obj, fields=[]):
        details = OrderedDict()
        for field_name in fields:
            accessor = Accessor(field_name)
            field = accessor.get_field(type(obj))
            if accessor is None:
                continue

            f_value = accessor.resolve(obj)
            if field:
                f_label = field.verbose_name[0].upper() + field.verbose_name[1:]
                f_type = (field.get_internal_type(),)
            else:
                f_type = "method" if callable(f_value) else "property"

            if f_type == "property":
                f_label = obj.get_property_label(accessor)
            elif f_type == "method":
                f_label = accessor

            details[field_name] = dict(
                name=field_name,
                field_type=f_type,
                label=f_label,
                value=f_value,
            )
        return details

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["details"] = self.get_details(obj, self.detail_fields)
        return context


class DetailView(
    DetailMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    TemplateMixin,
    DjangoDetailView,
):
    template_name_suffix = "_detail"

    def get(self, request, *args, **kwargs):
        self.detail_object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"{self.model._meta.verbose_name}"
        return context
