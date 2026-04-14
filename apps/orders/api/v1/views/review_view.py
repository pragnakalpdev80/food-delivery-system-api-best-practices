import logging
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from apps.orders.api.v1.serializers.review_serializers import ReviewSerializer
from common.utils.permissions import IsOrderCustomer
from common.api.filters import ReviewFilter
from common.api.throttles import ReviewCreateThrottle
from common.api.pagination import ReviewLimitOffsetPagination
from apps.orders.selectors.review_selector import ReviewSelector
from apps.orders.services.review_service import ReviewService

logger = logging.getLogger(__name__)

@extend_schema_view(
    create=extend_schema(
        summary="Review",
        description = "Review creation",
        request=ReviewSerializer,
        responses={
            201:{ReviewSerializer}
        },
        tags=['Review']
    ),
    list=extend_schema(
        summary="Review",
        description="Reviews",
        request=ReviewSerializer,
        responses={
            200:{ReviewSerializer}
        },
        tags=["Review"]
    ),
    retrieve=extend_schema(
        summary="Review",
        description="Review details",
        request=ReviewSerializer,
        responses={
            200:{ReviewSerializer}
        },
        tags=["Review"]
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):
    """ Reveiw ViewSet to manage to reviews. """
    permission_classes = [IsAuthenticated, IsOrderCustomer]
    pagination_class = ReviewLimitOffsetPagination
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ['rating',]
    ordering = ['-created_at']
    throttle_classes = [ReviewCreateThrottle]
    http_method_names = ['get', 'post']

    def get_queryset(self):
        """ Customers can only see their own reviews. """
        user = self.request.user
        if not user.is_authenticated:
            return ReviewSelector.get_none_review()
        return ReviewSelector.get_review_queryset(user=user)
    
    def perform_create(self, serializer):
        """ Customer can only review their own orders only. """
        customer_profile = self.request.user.customer_profile
        ReviewService.create(customer_profile=customer_profile, serializer=serializer)