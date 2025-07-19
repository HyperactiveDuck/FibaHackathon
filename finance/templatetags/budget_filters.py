from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """Template filter to look up dictionary values by key"""
    return dictionary.get(key, [])

@register.filter
def abs(value):
    """Template filter to get absolute value"""
    try:
        import builtins
        return builtins.abs(float(value))
    except (ValueError, TypeError):
        return 0