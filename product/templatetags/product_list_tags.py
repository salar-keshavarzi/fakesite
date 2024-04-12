from django import template
from product.models import Category, Brand

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def get_brands():
    return Brand.objects.all()
