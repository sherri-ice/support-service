from django.urls import path
from .views import TicketAPIView, TicketListAPIView, TicketAPICreateView

urlpatterns = [
    path('tickets/', TicketListAPIView.as_view(), name='tickets'),
    path('tickets/<int:pk>/', TicketAPIView.as_view()),
    path('tickets/add/', TicketAPICreateView.as_view(), name='create_ticket')
]
