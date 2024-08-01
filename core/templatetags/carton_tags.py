from django import template
from carton.cart import Cart
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def get_cart(context):
    request = context['request']
    return Cart(request)
