from crispy_forms.helper import FormHelper

from .viewsets.home import default_vs  # noqa

FormHelper.form_tag = False
FormHelper.include_media = False
