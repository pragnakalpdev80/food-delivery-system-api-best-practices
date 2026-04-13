import logging
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from apps.restaurants.api.v1.serializers.restaurant_serializers import  RestaurantSerializer, RestaurantDetailSerializer
from apps.restaurants.api.v1.serializers.menuitem_serializers import  MenuItemSerializer
from apps.restaurants.models import  Restaurant, MenuItem
from common.utils.permissions import IsRestaurantOwner, IsOwnerOrReadOnly
from common.api.pagination import RestaurantPageNumberPagination
from common.api.filters import RestaurantFilter

logger = logging.getLogger(__name__)


@extend_schema_view(
    create=extend_schema(
        summary="Restaurant",
        description = "Restaurant creation",
        request= RestaurantSerializer,
        responses={
            201:RestaurantSerializer
        },
        tags=['Restaurant']
    ),
    list=extend_schema(
        summary="Restaurant",
        description="Restaurants",
        tags=["Restaurant"],
        request= RestaurantSerializer,
        responses={
            200:RestaurantSerializer
        },
    ),
    retrieve=extend_schema(
        summary="Restaurant",
        description="Restaurant details",
        request= RestaurantDetailSerializer,
        responses={
            200:RestaurantDetailSerializer
        },
        tags=["Restaurant"]
    ),
    partial_update=extend_schema(
        summary="Update Restaurant Details",
        description=" Update your Restaurant details here",
        request= RestaurantSerializer,
        responses={
            200:RestaurantSerializer
        },
        tags=['Restaurant']
    ),
    destroy=extend_schema(
        summary="Restaurant",
        description = "We have added soft delete to delete Restaurant",
        responses={
            204:{}
        },
        tags=['Restaurant']
    ),
    menu=extend_schema(
        summary="Restaurant",
        description = "Restaurant Menu",
        request= MenuItemSerializer,
        responses={
            200:MenuItemSerializer
        },
        tags=['Restaurant']
    ),
    popular=extend_schema(
        summary="Restaurant",
        description = "Popular Restaurants",
        request= RestaurantSerializer,
        responses={
            200:RestaurantSerializer
        },
        tags=['Restaurant']
    ),
)
class RestaurantViewSet(viewsets.ModelViewSet):
    """ Driver ViewSet to manage restaurants. """
    permission_classes = [IsAuthenticated]
    pagination_class = RestaurantPageNumberPagination
    serializer_class = RestaurantDetailSerializer
    filterset_class = RestaurantFilter
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name', 'cuisine_type', 'description']
    ordering_fields = ['-average_rating', 'delivery_fee', 'created_at',]
    ordering = ['-created_at']
    http_method_names = ['get', 'post', 'patch','delete']

    def get_queryset(self):
        """
        Restaurant owners see only their own restaurant.
        All other authenticated users see all non-deleted restaurants.
        """
        user = self.request.user
        if not user.is_authenticated:
            return Restaurant.objects.none()
        if self.action in ['list', 'retrieve', 'menu', 'popular']:
            return Restaurant.objects.filter(is_deleted=False)
        return Restaurant.objects.filter(owner=user, is_deleted=False)
    
    def get_permissions(self):
        """
        Only restaurant owner can create, update and delete others can only see the details.
        """
        if self.action in ['list', 'retrieve', 'menu', 'popular']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsRestaurantOwner(), IsOwnerOrReadOnly()]

    def get_serializer_class(self):
        """
        When user searches for specific request then it will show the restaurant with menu items
        and for other methods it will show only restaurant details only.
        """
        if self.action == 'retrieve':
            return RestaurantDetailSerializer
        return RestaurantSerializer

    def perform_destroy(self, instance):
        """ Method to soft delete the restaurant. """
        instance.is_deleted = True
        menu_items = MenuItem.objects.filter(restaurant=instance.id,is_deleted=False)
        for menu_item in menu_items:
            menu_item.is_deleted = True
            menu_item.save()
        instance.save()

    @method_decorator(cache_page(60 * 5), name='list_restaurant')
    def list(self, request, *args, **kwargs):
        """ Overriden list method to get pagination on restaurants and added 5 minutes. """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = RestaurantSerializer(self.filter_queryset(self.get_queryset()), many=True, context={"request": request})
        return Response(serializer.data)
    
    @method_decorator(cache_page(60 * 10), name='retrieve_restaurant')
    def retrieve(self, request, *args, **kwargs):
        """ Added cache of 10 minutes on restaurant details method. """
        return super().retrieve(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 15), name='restaurant_menu')
    @action(detail=True, methods=['get'], url_path='menu')
    def menu(self, request,  *args, **kwargs):
        """ Created a custom menu method to get menu of the restaurant with 15 minutes of cache. """
        restaurant = self.get_object()
        items = MenuItem.objects.select_related('restaurant').filter(restaurant_id=restaurant.id, is_available=True)
          # print(items)
        serializer = MenuItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='popular')
    def popular(self, request,  *args, **kwargs):
        """ Created a custom method to get popular restaurants and added 30 minutes of cache on the method. """
        cache_key = 'popular_restaurant'
        cached_data = cache.get(cache_key)
        logger.info(cached_data)
        if cached_data is None:
            popular = Restaurant.objects.filter(is_open=True,is_deleted=False).order_by('-average_rating')
            serializer = RestaurantSerializer(popular, many=True, context={'request': request})
            cached_data = serializer.data
            cache.set(cache_key, cached_data, 1800)
        return Response(cached_data,status=status.HTTP_200_OK)
