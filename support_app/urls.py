from django.urls import path
from .views import RetrieveUpdateDestroyTicketAPIView, ListCreateTicketAPIView

urlpatterns = [
    path('tickets/', ListCreateTicketAPIView.as_view(), name='tickets'),
    path('tickets/<int:pk>/', RetrieveUpdateDestroyTicketAPIView.as_view(),
         name='ticket'),
    path('tickets/add/', ListCreateTicketAPIView.as_view(),
         name='create_ticket')
]
