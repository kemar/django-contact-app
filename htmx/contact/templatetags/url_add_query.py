from urllib.parse import parse_qs, urlsplit, urlunsplit

from django import template
from django.utils.http import urlencode


register = template.Library()


@register.simple_tag
def url_add_query(url, **kwargs):
    """
    Add or append a querystring param to the given URL.

    Usage:
        {% load url_add_query %}
        {% url_add_query request.get_full_path page=2 %}
    """
    url = urlsplit(url)
    new_qs = parse_qs(url.query) | kwargs
    return urlunsplit(url._replace(query=urlencode(new_qs, True)))
