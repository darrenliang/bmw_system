#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from django import template
register = template.Library()

from django.utils.html import format_html
@register.simple_tag
def circle_page(curr_page,loop_page):
    if not curr_page or not loop_page:
        return ''
    offset = abs(float(curr_page) - float(loop_page))
    if offset < 3:
        if curr_page == loop_page:
            page_ele = '<li value="%s" class="turn-page active"><a>%s</a></li>'%(loop_page,loop_page)
        else:
            page_ele = '<li value=%s class="turn-page"><a>%s</a></li>'%(loop_page,loop_page)
        return format_html(page_ele)
    else:
        return ''
