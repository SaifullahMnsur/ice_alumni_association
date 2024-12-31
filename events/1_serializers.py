from rest_framework import serializers
from .models import Event
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from rest_framework.reverse import reverse

# class EventSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Event
#         fields = [
#             'event_id', 'title', 'description', 'start_time', 'end_time', 
#             'location', 'status', 'created_at', 'updated_at', 'media_file'
#         ]
#         read_only_fields = ['created_at', 'updated_at']

#     def validate_event_id(self, value):
#         """Ensure that event_id follows the correct format."""
#         if not value.isalnum() and '-' not in value:
#             raise ValidationError("Event ID must only contain letters, numbers, and hyphens.")
#         return value

#     def create(self, validated_data):
#         """Handle file renaming logic during creation."""
#         event = super().create(validated_data)
#         return event

#     def update(self, instance, validated_data):
#         """Handle file renaming logic during update."""
#         event_id_changed = False
#         if 'event_id' in validated_data and validated_data['event_id'] != instance.event_id:
#             event_id_changed = True
        
#         # Update the instance with new data
#         instance = super().update(instance, validated_data)

#         # If event_id has changed, rename the media file accordingly
#         if event_id_changed:
#             instance.rename_media_files(instance.event_id)
#             instance.save()

#         return instance

class EventSerializer(serializers.ModelSerializer):
    detailed_url = serializers.SerializerMethodField()

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
            'detailed_url'
        ]

    def get_detailed_url(self, obj):
        request = self.context.get('request')
        return reverse('event-detail', kwargs={'event_id': obj.event_id}, request=request)


from rest_framework import serializers
from .models import Registration

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            'student_id', 'full_name', 'date_of_birth', 'batch', 'session', 'email', 'contact_number', 'whatsapp_number',
            'adult_guests', 'child_guests', 'total_amount', 'payment_method', 'transaction_id', 'transaction_document', 'profile_picture', 'password', 'event'
        ]