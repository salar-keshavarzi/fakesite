from rest_framework import serializers
from activity.models import Like


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'product')
        extra_kwargs = {
            'id': {'read_only': True}
        }
