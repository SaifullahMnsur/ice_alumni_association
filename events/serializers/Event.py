from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from rest_framework.reverse import reverse
from ..models.Event import Event

class EventSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'event_id',
            'title',
            'description',
            'start_time',
            'end_time',
            'location',
            'status',
            'created_at',
            'updated_at',
            'media_file',
            'details'
        ]

    def get_details(self, obj):
        request = self.context.get('request')
        return reverse('event-detail', kwargs={'event_id': obj.event_id}, request=request)