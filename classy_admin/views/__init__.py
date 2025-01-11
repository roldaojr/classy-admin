from .detail import DetailView
from .edit import CreateView, DeleteView, FormView, UpdateView
from .list import TableListView
from .dashboard import DashboardView
from .accounts import LoginView, LogoutView

__all__ = [
    "CreateView",
    "DeleteView",
    "DetailView",
    "TableListView",
    "UpdateView",
    "FormView",
    "DashboardView",
    "LoginView",
    "LogoutView",
]
