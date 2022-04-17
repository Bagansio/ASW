from django import template

register = template.Library()

@register.filter
def is_voted(id, votes):
    return id in votes

