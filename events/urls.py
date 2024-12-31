from django.urls import path
# from .views import EventDetailView, EventListView, EventRegistrationView, CalculateTotalAmountView
from .views.Event import EventDetailView, EventListView
from .views.Registration import EventRegistrationView, CalculateTotalAmountView

urlpatterns = [
    # Path to create a new event (using a POST request)
    # path('create/', CreateEventView.as_view(), name='create_event'),
    
    # Path to view the details of a single event (using the event ID)
    path('<str:event_id>/', EventDetailView.as_view(), name='event-detail'),
    
    # Path to list all events
    path('', EventListView.as_view(), name='event-list'),
    path('<slug:event_id>/register/', EventRegistrationView.as_view(), name='event-registration'),
    
    path('<slug:event_id>/calculate_total_amount/', CalculateTotalAmountView.as_view(), name='calculate-total-amount'),
]
