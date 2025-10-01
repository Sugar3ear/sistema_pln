from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Filtro para obtener un valor de un diccionario usando una clave"""
    if dictionary and key in dictionary:
        return dictionary.get(key)
    return {}

@register.filter
def dict_key_exists(dictionary, key):
    """Verificar si una clave existe en el diccionario"""
    if dictionary:
        return key in dictionary
    return False

@register.filter
def dict_items(dictionary):
    """Convertir diccionario a lista de items"""
    if dictionary:
        return dictionary.items()
    return []