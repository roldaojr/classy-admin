from types import SimpleNamespace


class Breadcrumb(SimpleNamespace):
    title: str

    def __str__(self):
        return self.title
