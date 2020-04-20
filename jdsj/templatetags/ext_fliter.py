from django import template
import json


register = template.Library()


@register.filter(name='rep_url')
def rep_url(value):
    return value.replace('n5/s54x54_jfs','n1/s540x540_jfs')