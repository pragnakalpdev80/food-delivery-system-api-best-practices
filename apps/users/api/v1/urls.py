from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    address_view,
    customer_view,
    driver_view,
    user_view
)

app_name = "users"

router = DefaultRouter()
router.register(r'customers', customer_view.CustomerViewSet, basename='customer')
router.register(r'addresses', address_view.AddressViewSet, basename='address')
router.register(r'drivers', driver_view.DriverViewSet, basename='driver')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', user_view.UserRegistrationView.as_view(), name='register'),
]