from ..registries import ViewSetRegistry
from ..viewsets.base import ViewSet

default_vs = ViewSet(name="default")

ViewSetRegistry.default_viewset = default_vs
