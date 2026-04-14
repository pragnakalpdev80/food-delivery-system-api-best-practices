import logging
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from apps.restaurants.api.v1.serializers.menuitem_serializers import  MenuItemSerializer
from apps.restaurants.selectors.menuitem_selector import MenuItemSelector
from common.utils.permissions import IsRestaurantOwner
from common.api.pagination import MenuItemPageNumberPagination
from common.api.filters import MenuItemFilter
from apps.restaurants.services.menuitem_service import MenuItemService

logger = logging.getLogger(__name__)

@extend_schema_view(
    create=extend_schema(
        summary="Menu Items",
        description = "Menu Items creation",
        request= MenuItemSerializer,
        responses={
            201:MenuItemSerializer
        },
        tags=['Menu Items']
    ),
    list=extend_schema(
        summary="Menu Items",
        description="Menu Item",
        request= MenuItemSerializer,
        responses={
            200:MenuItemSerializer
        },
        tags=["Menu Items"]
    ),
    retrieve=extend_schema(
        summary="Menu Items",
        description="Menu Item details",
        request= MenuItemSerializer,
        responses={
            200:MenuItemSerializer
        },
        tags=["Menu Items"]
    ),
    partial_update=extend_schema(
        summary="Update Menu Items",
        description=" Update your menu items details here",
        request= MenuItemSerializer,
        responses={
            200:MenuItemSerializer
        },
        tags=['Menu Items']
    ),
    destroy=extend_schema(
        summary="Menu Items",
        description = "We have added soft delete to delete Menu Items",
        responses={
            204:{}
        },
        tags=['Menu Items']
    ),
)
class MenuItemViewSet(viewsets.ModelViewSet):
    """ Menu items ViewSet to manage the menu items of restaurant. """
    pagination_class =MenuItemPageNumberPagination
    # queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filterset_class = MenuItemFilter
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'name', 'created_at',]
    ordering = ['-created_at']
    http_method_names = ['get', 'post', 'patch','delete']

    def get_permissions(self):
        """
        Permissions for authenticated users can see restaurants menu items and only restaurant owners can access all routes.
        """
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsRestaurantOwner()]

    def get_queryset(self):
        """
        Owners can create, update and delete own restaurants items.
        """
        if not self.request.user.is_authenticated:
            return MenuItemSelector.get_none_menu()
        user = self.request.user
        return MenuItemSelector.get_menuitem_queryset(user=user)

    def perform_destroy(self, instance):
        """ Method to soft delete the menu items. """
        MenuItemService.soft_delete_menu(item=instance)
        MenuItemService.clear_cache()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        MenuItemService.clear_cache()
        return response
    
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        MenuItemService.clear_cache()
        return response
    