from .detail import DetailView
from .edit import (
    CreateView,
    DeleteView,
    FormView,
    UpdateView,
)
from .list import TableListView

__all__ = [
    "CreateView",
    "DeleteView",
    "DetailView",
    "TableListView",
    "UpdateView",
    "FormView",
]
