from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
    """
    Splits the value into a list using the given key as delimiter.
    """
    return value.split(key)
