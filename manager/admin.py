from django.contrib import admin
from django.contrib.admin import register
from manager.models import StoryCategory, Story, ShippingPrice, Collection, Slider

from lib.base_model import CustomModelAdmin


class ManagerAdmin(admin.ModelAdmin):
    readonly_fields = ('created_time', 'modified_time', 'size')


class StoryInline(admin.TabularInline):
    model = Story
    extra = 0
    readonly_fields = ('is_active', 'size')


@register(StoryCategory)
class StoryCategoryAdmin(ManagerAdmin):
    list_display = ('id', 'title', 'size', 'is_active')
    search_fields = ('id', 'title')
    list_filter = ('is_active',)
    ordering = ('-is_active',)
    inlines = (StoryInline,)


@register(Story)
class StoryAdmin(ManagerAdmin):
    list_display = ('id', 'story_category', 'product', 'size', 'is_active')
    search_fields = ('id',)
    list_filter = ('is_active', 'story_category__title')
    ordering = ('-is_active',)


@register(ShippingPrice)
class ShippingPriceAdmin(CustomModelAdmin):
    list_display = ('id', 'price', 'is_active')
    list_filter = ('is_active',)
    ordering = ('-is_active',)


@register(Collection)
class CollectionAdmin(ManagerAdmin):
    list_display = ('id', 'category', 'size', 'is_active')
    list_filter = ('is_active',)
    ordering = ('-is_active',)


@register(Slider)
class SliderAdmin(ManagerAdmin):
    list_display = ('id', 'size', 'is_active')
    list_filter = ('is_active',)
    ordering = ('-is_active',)


