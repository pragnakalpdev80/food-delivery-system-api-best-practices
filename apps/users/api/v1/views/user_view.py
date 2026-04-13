import logging
import logging
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.api.v1.serializers.user_serializers import UserRegistrationSerializer
from apps.users.models import User

logger = logging.getLogger(__name__)

@extend_schema_view(
    post=extend_schema(
        summary="Registration",
        description=" Endpoint for new user registration of all types.",
        tags=["Userbase"],
        request=UserRegistrationSerializer,
        responses={
            201:UserRegistrationSerializer,
            400:{}
        }
    )
)
class UserRegistrationView(generics.CreateAPIView):
    """ User registration view to create/update and delete new user. """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Create method to create user and it will return user's data and refresh and access token.
        """
        serializer = self.get_serializer(data=request.data)   
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': serializer.data,  
            'refresh': str(refresh),  
            'access': str(refresh.access_token),  
        }, status=status.HTTP_201_CREATED)  
