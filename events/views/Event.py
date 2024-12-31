from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models.Event import Event
from ..serializers.Event import EventSerializer
from rest_framework.pagination import PageNumberPagination
    
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