from os import path
from string import Template

from django.utils.crypto import get_random_string
from django.utils.deconstruct import deconstructible
from django.utils.timezone import now


class LazyRandomString:
    def __init__(self, length):
        self.length = length

    def __str__(self):
        return get_random_string(self.length)


@deconstructible
class FormatStringUploadTo:
    """FileField upload_to function that use string format (string.format notation) to get file name"""

    def __init__(self, template: str, date_format: bool = False):
        self.template = template
        self.date_format = date_format

    def _render(self, context: dict) -> str:
        return self.template.format(**context)

    def __call__(self, instance, filename) -> str:
        dirname = path.dirname(filename)
        basename, ext = path.splitext(path.basename(filename))
        upload_path = self._render(
            dict(
                filename=filename,
                instance=instance,
                dirname=dirname,
                basename=basename,
                ext=ext[1:],
                random_text=LazyRandomString(16),
            )
        ).strip("/")
        if self.date_format:
            return now().strftime(upload_path)
        return upload_path


class TemplateStringUploadTo(FormatStringUploadTo):
    """FileField upload_to function that use Template string ($ notation) to get file name"""

    def _render(self, context: dict) -> str:
        template = Template(self.template)
        return template.safe_substitute(**context)
