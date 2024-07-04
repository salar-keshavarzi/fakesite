from product.models import Product
from django import template
from manager.models import StoryCategory, Collection, Slider

register = template.Library()


@register.simple_tag
def get_recent_products():
    return Product.get_recent_adds()


@register.simple_tag
def get_offers_products():
    return Product.get_offers()


@register.simple_tag
def get_story_categories():
    return StoryCategory.objects.all()


@register.simple_tag
def get_collections():
    return Collection.objects.all()


@register.simple_tag
def get_sliders():
    return Slider.objects.all()
