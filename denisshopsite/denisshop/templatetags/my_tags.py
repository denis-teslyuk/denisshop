from django import template
from django.core.exceptions import ObjectDoesNotExist

from cart.models import Cart

register = template.Library()

@register.simple_tag()
def get_free_keys(item):
    return item.game.keys.filter(user=None).count()