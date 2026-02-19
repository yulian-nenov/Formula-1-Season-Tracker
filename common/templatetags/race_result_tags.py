from django import template

register = template.Library()

@register.filter
def podium_position(position: int|str) -> str:
    if position == 1:
        return 'gold'
    elif position == 2:
        return 'silver'
    elif position == 3:
        return 'bronze'
    elif position is None:
        return 'out-of-race'
    return ''
