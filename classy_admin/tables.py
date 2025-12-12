from django.utils.html import escape, format_html
from django_tables2 import columns
from django_tables2.utils import AttributeDict


class BooleanColumn(columns.BooleanColumn):
    def render(self, value, record, bound_column):
        value = self._get_bool_value(record, value, bound_column)
        text = "Sim" if value else "Não"
        badge_class = "success" if value else "danger"
        attrs = {"class": f"badge badge-light-{badge_class} fs-6"}
        attrs.update(self.attrs.get("span", {}))
        return format_html(
            "<span {}>{}</span>", AttributeDict(attrs).as_html(), escape(text)
        )
