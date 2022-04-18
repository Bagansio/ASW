from django import template

register = template.Library()

@register.filter
def is_voted(id, votes):
    return id in votes

@register.filter
def is_url(submission):
    return submission.is_url()

@register.filter
def pretty_url(url):
    pr, path = url.split('://')

    if path is None:
        return pr
    return path
