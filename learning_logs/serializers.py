from rest_framework import serializers

from learning_logs.models import Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['color', 'title']
