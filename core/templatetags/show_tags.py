# core/templatetags/custom_tags.py
from django import template
from core.models import Category, Maqola
from django.contrib.auth import get_user_model

register = template.Library()

@register.inclusion_tag('core/list_cats.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('core/list_cats_copy.html')
def show_user(cat_selected=0):
    users = get_user_model().objects.all()
    return {'users': users, 'cat_selected': cat_selected}

@register.inclusion_tag('core/list_cats_main.html')
def show_user_for_main(cat_selected=0):
    users = get_user_model().objects.all()
    return {'users': users, 'cat_selected': cat_selected}