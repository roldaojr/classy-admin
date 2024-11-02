from django.conf import settings
from django.http import JsonResponse
from django.utils.module_loading import import_string
from django_select2.views import AutoResponseView


class CustomSelect2ResponseView(AutoResponseView):
    def get(self, request, *args, **kwargs):
        self.widget = self.get_widget_or_404()
        self.term = kwargs.get("term", request.GET.get("term", ""))
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse(
            {
                "results": [
                    {"text": obj["_text"], "id": obj["_id"]}
                    for obj in context["object_list"]
                ],
                "more": context["page_obj"].has_next(),
            },
            encoder=import_string(settings.SELECT2_JSON_ENCODER),
        )
