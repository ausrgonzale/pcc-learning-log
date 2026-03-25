from rest_framework import serializers

from .models import Topic, Entry


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = [
            'id',
            'text',
            'date_added',
        ]


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = [
            'id',
            'text',
            'date_added',
            'topic',
        ]