from django.urls import path
from activity.views import ProductCommentView, CommentReplyView
urlpatterns = [
    path('<str:product_id>/comment/add/', ProductCommentView.as_view(), name='add_comment'),
    path('<str:comment_id>/reply/add/', CommentReplyView.as_view(), name='add_reply')
]

