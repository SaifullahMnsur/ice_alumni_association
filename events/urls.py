from django.urls import path
# from .views import EventDetailView, EventListView, EventRegistrationView, CalculateTotalAmountView
# from .views.Event import EventDetailView, EventListView
# from .views.Registration import EventRegistrationView
from .views import Event
from .views import Registration

urlpatterns = [
    
    # Path to view the details of a single event (using the event ID)
    path('<str:event_id>/', Event.EventDetailView.as_view(), name='event-detail'),
    
    # Path to list all events
    path('', Event.EventListView.as_view(), name='event-list'),
    path('<slug:event_id>/register/', Registration.EventRegistrationView.as_view(), name='event-registration'),
    
    path('<slug:event_id>/calculate_total_amount/', Event.CalculateTotalAmountView.as_view(), name='calculate-total-amount'),
    path('<slug:event_id>/payment-methods/', Event.PaymentMethodsAPIView.as_view(), name='calculate-total-amount'),
]
