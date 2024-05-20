from django import template
from django.shortcuts import reverse
from urllib.parse import urlencode

register = template.Library()


@register.simple_tag(takes_context=True)
def is_active(context, *paths):
    request = context['request']
    return request.path in paths


@register.filter
def add_text(value, text):
    if value:
        return f"{value} {text}"
    return "N/A"


@register.simple_tag(takes_context=True)
def change_lang_url(context, lang_code):
    request = context['request']
    next_url = request.path
    url = next_url.split("/")
    url[1] = lang_code
    full_url = '/'.join(url)
    return full_url
