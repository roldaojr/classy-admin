class ActionTabsViewMixin:
    def get_context_data(self, **kwargs):
        tabs = [
            dict(
                title=getattr(action, "verbose_name", None),
                url=self.urls.get(name),
                action=name,
            )
            for name, action in self.viewset.actions.items()
            if getattr(action, "tab", False)
        ]
        return super().get_context_data(tabs=tabs, **kwargs)
