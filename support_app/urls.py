from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TicketAPIView, TicketListAPIView


urlpatterns = [
    path('tickets/', TicketListAPIView.as_view(), name='tickets'),
    path('tickets/<int:pk>/', TicketAPIView.as_view())
]
