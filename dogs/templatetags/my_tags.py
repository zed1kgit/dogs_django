from django import template

register = template.Library()

@register.filter
def dogs_media(value):
    if value:
        return fr'/media/{value}'
    return '/static/dummydog.jpg'

@register.filter
def user_media(value):
    if value:
        return fr'/media/{value}'
    return '/static/noavatar.png'