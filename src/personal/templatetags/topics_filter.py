from django import template
from typing import Any

register = template.Library()

@register.filter
def previous(some_list, current_index):
    try:
        return some_list[int(current_index) - 1] # access the previous element
    except:
        return ''