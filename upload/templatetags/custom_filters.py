from django import template
import re

register = template.Library()

@register.filter
def regex_search(string, pattern):
    return bool(re.search(pattern, string))
