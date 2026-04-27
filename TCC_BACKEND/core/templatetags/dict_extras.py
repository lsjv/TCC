from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def list_index(lst, idx):
    """Retorna lst[idx] — permite acessar listas por índice nos templates."""
    try:
        return lst[int(idx)]
    except (IndexError, TypeError, ValueError):
        return ''


@register.filter
def make_tuple(a, b):
    """Cria uma tupla (a, b) para verificação em sets nos templates."""
    return (a, b)