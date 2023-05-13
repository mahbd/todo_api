from rest_framework import serializers

from .models import Tag, Change


class TagSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tag
        fields = ['id', 'user', 'title']
        read_only_fields = ['id']


class ChangeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Change
        fields = ['id', 'user', 'table', 'data_id', 'action']
        read_only_fields = ['id']
