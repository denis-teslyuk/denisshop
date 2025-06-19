from django import template

register = template.Library()

@register.simple_tag()
def get_free_keys(item):
    return item.game.keys.filter(user=None).count()
