from django import template

register = template.Library()

@register.filter
def cop(value):
    try:
        n = int(value)
    except (TypeError, ValueError):
        return value
    return f"{n:,}".replace(",", ".")
