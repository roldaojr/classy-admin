from django.db.models import Model
from django_tables2 import columns, tables
from django_tables2.utils import Accessor


def table_factory(model: Model, fields=None, url_name=None, extra_attrs=None):
    attrs = {"Meta": type("Meta", (object,), {"model": model, "fields": fields})}

    if fields is None:
        fields = []
    for field_name in fields:
        field = Accessor(field_name).get_field(model)
        if field is None:
            # not a field, may be attribute
            attr = getattr(model, field_name)
            verbose_name = getattr(attr, "verbose_name", None)
            if verbose_name is not None:
                column = columns.library.column_for_field(field)
                column_type = type(column)
                attrs[field_name] = column_type(
                    verbose_name=verbose_name, orderable=False
                )

    if url_name is not None:
        linked_field = fields[0] if fields else "id"
        field = Accessor(linked_field).get_field(model)
        column = columns.library.column_for_field(field)
        column_type = type(column)
        link = (url_name, {"pk": Accessor("pk")})
        attrs.update({linked_field: column_type(linkify=link)})

    if extra_attrs is not None:
        attrs.update(extra_attrs)
    return type("%sTable" % model._meta.object_name, (tables.Table,), attrs)
