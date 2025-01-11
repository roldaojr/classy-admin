from django.db.models.base import ModelBase
from django.db.models.options import Options

from ..views.detail import DetailView
from ..views.edit import CreateView, DeleteView, UpdateView
from ..views.list import TableListView
from .actions import Action
from .base import ViewSet, view_with_action
from .mixins import WithActionMixin


class CrudListViewMixin:
    viewset: "CrudViewSet"

    @property
    def list_display(self):
        return self.viewset.get_list_display()

    @property
    def filterset_class(self):
        return self.viewset.filterset_class

    @property
    def filterset_fields(self):
        return self.viewset.filterset_fields


class CrudFormViewMixin:
    viewset: "CrudViewSet"

    @property
    def fields(self):
        return self.viewset.get_form_fields()

    @property
    def exclude(self):
        return self.viewset.get_form_exclude()

    @property
    def form_class(self):
        return self.viewset.get_form_class(self)


class CrudListView(CrudListViewMixin, TableListView):
    pass


class CrudCreateView(CrudFormViewMixin, CreateView):
    pass


class CrudUpdateView(CrudFormViewMixin, UpdateView):
    pass


class CrudDeleteView(DeleteView):
    pass


class CrudDetailView(DetailView):
    viewset: "CrudViewSet"

    def get_detail_fields(self):
        detail_fields = self.viewset.get_detail_fields()
        if detail_fields:
            return detail_fields
        fields = self.viewset.get_form_fields()
        if fields:
            return fields
        if self.viewset.model:
            model_opts: Options = self.viewset.model._meta
            return [field.name for field in model_opts._get_fields(reverse=False)]


class CrudViewSet(ViewSet):
    list_display = None
    fields = None
    detail_fields = None
    exclude = None
    form_class = None
    filterset_class = None
    filterset_fields = None

    available_actions: dict[str, Action] = dict(
        list=Action(view_class=CrudListView),
        add=Action(view_class=CrudCreateView),
        change=Action(view_class=CrudUpdateView, default=True),
        detail=Action(view_class=CrudDetailView, default=False),
        delete=Action(view_class=CrudDeleteView),
    )

    def __init__(
        self,
        model: ModelBase = None,
        name: str = None,
        register: bool = True,
        **kwargs,
    ):
        super().__init__(model, name, register, **kwargs)
        available_actions = self.get_available_actions()
        for name in available_actions.keys():
            action = available_actions.get(name)
            kwargs = {attr: val for attr, val in action.__dict__.items()}
            view_class = view_with_action(kwargs.get("view_class"))
            kwargs.update({"viewset": self, "view_class": view_class})
            self._update_action_kwargs(name, kwargs)
            self._actions[name] = Action(name=name, **kwargs)

    def get_available_actions(self) -> dict[str, Action]:
        return self.available_actions

    def get_list_display(self) -> list[str] | None:
        return self.list_display

    def get_detail_fields(self) -> list[str] | None:
        return self.detail_fields

    def get_form_class(self, view: WithActionMixin):
        return self.form_class

    def get_form_fields(self) -> list[str] | None:
        return self.fields

    def get_form_exclude(self) -> list[str] | None:
        return self.exclude
