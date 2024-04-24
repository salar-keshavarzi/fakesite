from django.urls import path
from account.views import UserPanelPersonalView, \
    UserPanelBuysListView, UserPanelTransactionsListView, UserPanelAddressesListView, UserPanelSupportView, \
    UserPanelCommentsView, UserPanelLikesView, UserPanelAddressCreateView, UserPanelAddressDeleteView, \
    UserPanelAddressEditView, UserPanelCommentDeleteView, UserPanelLikeDeleteView, UserPanelSupportClearView

urlpatterns = [
    path('panel/', UserPanelPersonalView.as_view(), name="user_panel"),
    path('panel/orders/list/', UserPanelBuysListView.as_view(), name="user_panel_buys"),
    path('panel/transacions/list/', UserPanelTransactionsListView.as_view(), name="user_panel_transactions"),
    path('panel/address/list/', UserPanelAddressesListView.as_view(), name="user_panel_addresses"),
    path('panel/address/create/', UserPanelAddressCreateView.as_view(), name="user_address_create"),
    path('panel/address/<int:address_id>/delete/', UserPanelAddressDeleteView.as_view(), name="user_address_delete"),
    path('panel/address/<int:address_id>/edit/', UserPanelAddressEditView.as_view(), name="user_address_edit"),
    path('panel/support/', UserPanelSupportView.as_view(), name="user_panel_support"),
    path('panel/support/clear/', UserPanelSupportClearView.as_view(), name="user_support_clear"),
    path('panel/comments/', UserPanelCommentsView.as_view(), name="user_panel_comments"),
    path('panel/comment/<int:comment_id>/delete/', UserPanelCommentDeleteView.as_view(), name="user_comment_delete"),
    path('panel/favorites/', UserPanelLikesView.as_view(), name="user_panel_likes"),
    path('panel/favorite/<int:like_id>/delete/', UserPanelLikeDeleteView.as_view(), name="user_like_delete"),
]
