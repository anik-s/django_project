from django import template
from django.utils.html import escape

register = template.Library()


@register.filter
def formatted_sub_categories(sub_categories):
    p_cats = []
    for c in sub_categories:
        p_cats.append(c.category.name)
    return escape("{0}".format(', '.join(p_cats)))