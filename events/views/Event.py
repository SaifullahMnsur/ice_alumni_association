from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models.Event import Event
from ..serializers.Event import EventSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
    
class EventListView(APIView):
    class EventPagination(PageNumberPagination):
        page_size = 10  # Set the default number of items per page
        page_size_query_param = 'page_size'  # Allow clients to control the page size via query parameter
        max_page_size = 100  # Maximum page size the client can request

    def get(self, request, *args, **kwargs):
        events = Event.objects.all()  # Fetch all events
        paginator = self.EventPagination()
        paginated_events = paginator.paginate_queryset(events, request)
        serializer = EventSerializer(paginated_events, context={'request': request}, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class EventDetailView(APIView):
    def get(self, request, *args, **kwargs):
        event_id = self.kwargs.get('event_id')
        event = get_object_or_404(Event, event_id=event_id)  # Fetch the specific event
        serializer = EventSerializer(event, context={'request': request})  # Serialize the event
        return Response(serializer.data)  # Return the serialized event data as JSON

class CalculateTotalAmountView(APIView):
    def get(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id')
        child_guests = int(request.query_params.get('child_guests', 0))
        adult_guests = int(request.query_params.get('adult_guests', 0))

        event = get_object_or_404(Event, event_id=event_id)
        total_amount = event.amount_per_person + event.amount_per_adult_guest * adult_guests + event.amount_per_child_guest * child_guests
        return Response({'total_amount': total_amount})

class PaymentMethodsAPIView(APIView):
    """
    API view to fetch payment methods for a specific event.
    """

    def get(self, request, event_id):
        try:
            event = Event.objects.get(event_id=event_id)
        except Event.DoesNotExist:
            raise NotFound(detail="Event not found.")

        payment_methods = {
            "bkash": {
                "account_number": event.bkash_account_number,
                "payment_option": event.bkash_payment_option,
            },
            "nagad": {
                "account_number": event.nagad_account_number,
                "payment_option": event.nagad_payment_option,
            },
            "rocket": {
                "account_number": event.rocket_account_number,
                "payment_option": event.rocket_payment_option,
            },
            "bank": {
                "account_name": event.bank_account_name,
                "account_number": event.bank_account_number,
                "bank_name": event.bank_name,
                "branch_name": event.bank_branch_name,
                "swift_code": event.bank_swift_code,
                "routing_number": event.bank_routing_number,
                "city": event.bank_city,
                "country": event.bank_country,
            },
        }

        # Remove empty fields
        for key, value in payment_methods.items():
            payment_methods[key] = {k: v for k, v in value.items() if v}

        return Response(payment_methods)