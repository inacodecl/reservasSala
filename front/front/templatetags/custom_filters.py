from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Filtro para acceder a un diccionario desde la plantilla."""
    return dictionary.get(key)