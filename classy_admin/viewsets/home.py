from ..viewsets.base import ViewSet
from ..registries import ViewSetRegistry

default_vs = ViewSet(name="default")

ViewSetRegistry.default_viewset = default_vs
