from rest_framework import serializers
from ..models.Registration import Registration

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = [
            'student_id', 'full_name', 'date_of_birth', 'batch', 'session', 'email', 'contact_number', 'whatsapp_number',
            'adult_guests', 'child_guests', 'total_amount', 'payment_method', 'transaction_id', 'transaction_document', 'profile_picture', 'password', 'event'
        ]