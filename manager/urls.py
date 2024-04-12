from django.urls import path
from manager.views import StoryListAPI

urlpatterns = [
    path('storyCategory/<int:story_category_id>/api/', StoryListAPI.as_view(), name="story_list_api"),
]
