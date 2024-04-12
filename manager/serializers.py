from rest_framework import serializers
from manager.models import Story, StoryCategory


class StorySerializer(serializers.ModelSerializer):
    product_id = serializers.CharField(source='product.id', read_only=True)

    class Meta:
        model = Story
        fields = ('id', 'image', 'product_id')
        extra_kwargs = {
            'id': {'read_only': True},
            'image': {'read_only': True},
        }


class StoryCategorySerializer(serializers.ModelSerializer):
    stories = StorySerializer(many=True)

    class Meta:
        model = StoryCategory
        fields = ('id', 'title', 'image', 'stories')
        extra_kwargs = {
            'id': {'read_only': True},
            'title': {'read_only': True},
            'image': {'read_only': True},
            'stories': {'read_only': True},
        }
