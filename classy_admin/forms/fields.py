from functools import partial
from itertools import groupby

from django import forms
from django.utils.translation import gettext_lazy as _


class GroupedModelChoiceIterator(forms.models.ModelChoiceIterator):
    def __init__(self, field, groupby):
        self.groupby = groupby
        super().__init__(field)

    def __iter__(self):
        if self.field.empty_label is not None:
            yield ("", self.field.empty_label)
        queryset = self.queryset

        # Can't use iterator() when queryset uses prefetch_related()
        if not queryset._prefetch_related_lookups:
            queryset = queryset.iterator()
        for group, objs in groupby(queryset, self.groupby):
            yield (group, [self.choice(obj) for obj in objs])


class PermissionsChoiceField(forms.ModelMultipleChoiceField):
    widget = forms.CheckboxSelectMultiple

    def __init__(self, *args, **kwargs):
        def groupby(perm):
            model_class = perm.content_type.model_class()
            if model_class:
                model_name = str(
                    getattr(
                        model_class._meta,
                        "verbose_name_plural",
                        perm.content_type.model,
                    )
                )
            else:
                model_name = str(perm.content_type.model)
            return model_name.capitalize()

        self.iterator = partial(GroupedModelChoiceIterator, groupby=groupby)
        super().__init__(*args, **kwargs)

    def label_from_instance(self, perm):
        model_class = perm.content_type.model_class()
        model_name = (
            getattr(model_class._meta, "verbose_name", perm.content_type.model)
            if model_class
            else perm.content_type.model
        ).capitalize()

        permission_labels = {
            "add": "Pode adicionar {model_name}",
            "change": "Pode mudar {model_name}",
            "view": "Pode visualizar {model_name}",
            "delete": "Pode deletar {model_name}",
        }

        for key in permission_labels.keys():
            if perm.codename.startswith(key):
                return permission_labels[key].format(model_name=model_name)

        return _(perm.name)
