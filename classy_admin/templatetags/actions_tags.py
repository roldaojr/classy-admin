from django import template

from ..viewsets.actions import Action

register = template.Library()


@register.simple_tag(takes_context=True)
def action_check(context, action: Action, obj=None):
    """
    Check if current user has specified permission.

    Use:
    {% action_check action object as allowed %}
    {% if allowed %}
        ...
    {% endif %}
    """
    request = context.get("request", None)
    check_func = action.check or Action.check
    return check_func(action, request, obj)
