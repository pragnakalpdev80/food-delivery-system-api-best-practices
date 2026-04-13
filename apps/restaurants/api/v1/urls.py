from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    restaurant_view,
    menuitem_view
)

app_name = "restaurants"

router = DefaultRouter()
router.register(r'restaurants', restaurant_view.RestaurantViewSet, basename='restaurant')
router.register(r'menu-items', menuitem_view.MenuItemViewSet, basename='menu-item')

urlpatterns = [
    path('', include(router.urls)),
]