from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView
from manager.serializers import StoryCategorySerializer
from manager.models import StoryCategory


class StoryListAPI(RetrieveAPIView):
    serializer_class = StoryCategorySerializer
    queryset = StoryCategory.objects.all()
    lookup_url_kwarg = 'story_category_id'
