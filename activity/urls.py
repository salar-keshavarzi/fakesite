from django.urls import path
from activity.views import ProductCommentView, CommentReplyView, AddToFavoriteAPI, DeleteFavoriteAPI

urlpatterns = [
    path('<str:product_id>/comment/add/', ProductCommentView.as_view(), name='add_comment'),
    path('<str:comment_id>/reply/add/', CommentReplyView.as_view(), name='add_reply'),
    path('<int:user_id>/favorite/create/api/', AddToFavoriteAPI.as_view(), name='add_favorite_api'),
    path('<int:user_id>/favorite/<int:favorite_id>/delete/api/', DeleteFavoriteAPI.as_view(), name='remove_favorite_api'),
]
