from django.db import models
from django.utils.functional import cached_property
from django.utils.text import smart_split, unescape_string_literal
from django.views.generic import ListView as DjangoListView
from django_filters.views import FilterMixin as BaseFilterMixin
from django_tables2 import SingleTableMixin

from ..viewsets.base import WithActionMixin
from .aaa import LoginRequiredMixin, PermissionRequiredMixin
from .list_table import table_factory
from .mixins import TemplateMixin


class FilterMixin(BaseFilterMixin):
    @cached_property
    def filterset(self):
        filterset_class = self.get_filterset_class()
        if filterset_class:
            return self.get_filterset(filterset_class)

    def get_filtered_queryset(self):
        if self.filterset:
            return self.filterset.qs
        return self.get_queryset()

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            object_list=self.get_filtered_queryset(),
            filter=self.filterset,
        )


class FilteredSingleTableMixin(FilterMixin, SingleTableMixin):
    list_display = None
    filterset_fields = []

    def get_list_display(self):
        return self.list_display

    def get_table_class(self):
        default_action = self.actions.item_default
        if not self.table_class:
            return table_factory(
                self.model,
                self.get_list_display(),
                url_name=default_action.url_name if default_action else None,
            )
        return super().get_table_class()

    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        table.order_by = self.get_table_order_by(table)
        return table

    def get_table_pagination(self, table):
        pagination = super().get_table_pagination(table)
        updates = {"page": self.request.GET.get("page")}
        if not isinstance(pagination, dict):
            pagination = {}
        pagination.update(updates)
        return pagination

    def get_table_data(self):
        return self.get_filtered_queryset()

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get("per_page", None)
        if per_page is not None:
            self.request.session["per_page"] = per_page
        return self.request.session.get("per_page", self.paginate_by)

    def get_table_order_by(self, table):
        order_key = f"user-settings/{self.request.path}/order"
        req_order_by = self.request.GET.getlist(table.prefixed_order_by_field)
        if not req_order_by:
            req_order_by = []
        saved_order_by = self.request.session.get(order_key, [])
        new_order_by = req_order_by + [
            f
            for f in saved_order_by
            if f not in req_order_by and f"-{f}" not in req_order_by
        ]
        self.request.session[order_key] = new_order_by
        return new_order_by


class SearchMixin:
    search_fields = []

    def filter_queryset(self, queryset):
        orm_lookups = [
            f"{str(search_field)}__icontains" for search_field in self.search_fields
        ]
        or_query = models.Q()
        search_term = self.request.GET.get("search", "")
        for bit in smart_split(search_term):
            if bit.startswith(('"', "'")) and bit[0] == bit[-1]:
                bit = unescape_string_literal(bit)
            for orm_lookup in orm_lookups:
                or_query |= models.Q((orm_lookup, bit))
        return queryset.filter(or_query)

    def get_queryset(self):
        return self.filter_queryset(super().get_queryset())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_search_input_placeholder"] = ", ".join(
            [
                str(self.model._meta.get_field(f).verbose_name)
                for f in self.search_fields
            ]
        )
        return context


class ListView(
    WithActionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    FilterMixin,
    SearchMixin,
    TemplateMixin,
    DjangoListView,
):
    template_name_suffix = "_list"

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            page_title=self.model._meta.verbose_name_plural.capitalize(), **kwargs
        )


class TableListView(
    WithActionMixin,
    LoginRequiredMixin,
    PermissionRequiredMixin,
    FilteredSingleTableMixin,
    SearchMixin,
    TemplateMixin,
    DjangoListView,
):
    template_name_suffix = "_list"

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            page_title=self.model._meta.verbose_name_plural.capitalize(),
            **kwargs,
        )
