from django.forms.widgets import TextInput


class DateInput(TextInput):
    input_type = "date"
    template_name = "django/forms/widgets/text.html"


class DateTimeInput(TextInput):
    input_type = "datetime-local"
    template_name = "django/forms/widgets/text.html"
