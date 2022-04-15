from django.urls import path
from .views import RetrieveUpdateDestroyTicketAPIView, ListCreateTicketAPIView, \
    AddMessageToTicketAPIView

urlpatterns = [
    path('tickets/', ListCreateTicketAPIView.as_view(), name='tickets'),
    path('tickets/<int:pk>/', RetrieveUpdateDestroyTicketAPIView.as_view(),
         name='ticket'),
    path('tickets/add/', ListCreateTicketAPIView.as_view(),
         name='create_ticket'),
    path('tickets/<int:pk>/new_message/', AddMessageToTicketAPIView.as_view(),
         name='add_new_message_to_ticket')
]
