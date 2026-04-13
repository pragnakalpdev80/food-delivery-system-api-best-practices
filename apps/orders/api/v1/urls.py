from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    cart_view,
    cartitem_view,
    order_view,
    orderitem_view,
    review_view
)

app_name = "orders"

router = DefaultRouter()
router.register(r'orders', order_view.OrderViewSet, basename='order')
router.register(r'order-items', orderitem_view.OrderItemViewSet, basename='orderitem')
router.register(r'reviews', review_view.ReviewViewSet, basename='review')
router.register(r'cart', cart_view.CartViewSet, basename='cart')
router.register(r'cart-items', cartitem_view.CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
]