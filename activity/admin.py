from django.contrib import admin
from django.contrib.admin import register
from activity.models import Like, Comment, Reply, Support

from lib.base_model import CustomModelAdmin


class MessageReplyInline(admin.TabularInline):
    model = Reply
    extra = 1
    readonly_fields = ('user', 'is_active')


@register(Like)
class LikeAdmin(CustomModelAdmin):
    list_display = ('id', 'user', 'product')
    search_fields = ('id', 'user__id', 'user__username')


@register(Comment)
class CommentAdmin(CustomModelAdmin):
    list_display = ('id', 'user', 'product')
    search_fields = ('id', 'user__id', 'user__username', 'product__id')
    inlines = (MessageReplyInline, )

@register(Reply)
class ReplyAdmin(CustomModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('id', 'user__id', 'user__username')


@register(Support)
class SupportAdmin(CustomModelAdmin):
    list_display = ('id', 'user', 'created_time', 'is_answered')
    list_filter = ('is_answered',)
    search_fields = ('id', 'user__id', 'user__username')
    ordering = ('-created_time',)

    def get_readonly_fields(self, request, obj=None):
        return ('created_time', 'modified_time', 'is_answered')
