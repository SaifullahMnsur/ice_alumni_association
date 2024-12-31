
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models.Event import Event
from ..models.Registration import Registration
from ..serializers.Registration import RegistrationSerializer

class EventRegistrationView(APIView):
    def post(self, request, event_id, *args, **kwargs):
        # Fetch the Event object based on event_id
        event = get_object_or_404(Event, event_id=event_id)
        
        # Prepare the data to create a Registration
        data = request.data.copy()
        # data['event'] = event.event_id  # Automatically set the event based on the event_id
        data['event_id'] = event_id  # Automatically set the event based on the event_id
        
        # Create the Registration instance and validate
        serializer = RegistrationSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            registration = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print("Error invalid serializer")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CalculateTotalAmountView(APIView):
    def get(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id')
        child_guests = int(request.query_params.get('child_guests', 0))
        adult_guests = int(request.query_params.get('adult_guests', 0))

        event = get_object_or_404(Event, event_id=event_id)
        total_amount = event.amount_per_person + event.amount_per_adult_guest * adult_guests + event.amount_per_child_guest * child_guests
        return Response({'total_amount': total_amount})

class RegistrationApprovalView(APIView):
    def patch(self, request, *args, **kwargs):
        registration_id = kwargs.get('pk')
        registration = get_object_or_404(Registration, id=registration_id)

        # Update the approval status
        registration.approved = True
        registration.save()

        # Send email to student
        registration.send_approval_email()

        return Response({'message': 'Registration approved and email sent.'}, status=status.HTTP_200_OK)

class RegistrationCheckView(APIView):
    def get(self, request, *args, **kwargs):
        student_id = request.query_params.get('student_id')
        password = request.query_params.get('password')
        
        registration = get_object_or_404(Registration, student_id=student_id)

        if registration.check_password(password):
            return Response({'approved': registration.approved, 'event': registration.event.title})
        else:
            return Response({'error': 'Invalid ID or Password'}, status=status.HTTP_400_BAD_REQUEST)
