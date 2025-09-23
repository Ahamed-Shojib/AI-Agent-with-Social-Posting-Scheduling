from rest_framework import serializers
from .models import ScheduledPost

class ScheduledPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledPost
        fields = (
            'id', 
            'text_content', 
            'image', 
            'scheduled_time', 
            'target_platforms', 
            'status',
            'published_at'
        )
        read_only_fields = ('status', 'published_at',)

class HashtagSuggestionSerializer(serializers.Serializer):
    text_content = serializers.CharField()
    suggested_hashtags = serializers.ListField(
        child=serializers.CharField(), 
        read_only=True
    )
