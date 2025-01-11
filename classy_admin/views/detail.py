from collections import OrderedDict

from django.db.models.fields import Field
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
            if accessor is None:
                continue
            f_value = accessor.resolve(obj)

            # check if target is a field
            field: Field = accessor.get_field(type(obj))
            if field:
                # target attribute is a field
                f_label = field.verbose_name.capitalize()
                f_type = field.get_internal_type()
                # if has choices get choice label for value
                if field.choices:
                    f_value = dict(field.choices).get(f_value)
            else:
                # target attribute is not a field
                if callable(f_value):
                    f_type = "method"
                    f_label = getattr(f_value, "short_description", field_name)
                else:
                    f_type = "property"
                    propoerty_obj = getattr(type(obj), field_name, None)
                    if propoerty_obj:
                        f_label = getattr(
                            propoerty_obj, "short_description", field_name
                        )

            if f_type == "property":
                f_label = obj.get_property_label(accessor)
            elif f_type == "method":
                f_label = getattr(f_value, "short_description", field_name)

            details[field_name] = dict(
                name=field_name,
                field_type=f_type,
                label=f_label,
                value=f_value,
            )
        return details

    def get_detail_fields(self):
        return self.detail_fields

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["details"] = self.get_details(obj, self.get_detail_fields())
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
