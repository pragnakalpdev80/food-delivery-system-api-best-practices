# apps/health/views.py
from django.db import connection
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    create=extend_schema(
        summary="Health",
        description = "Health Check endpoint",
        tags=['Health'],
    )
)
class HealthCheckView(APIView):
    permission_classes = []  # Allow unauthenticated access
    
    def get(self, request):
        health_status = {
            'status': 'healthy',
            'checks': {}
        }
        
        # Database check
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            health_status['checks']['database'] = 'ok'
        except Exception as e:
            health_status['status'] = 'unhealthy'
            health_status['checks']['database'] = f'error: {str(e)}'
        
        # Redis check
        try:
            cache.set('health_check', 'ok', 10)
            cache.get('health_check')
            health_status['checks']['redis'] = 'ok'
        except Exception as e:
            health_status['status'] = 'unhealthy'
            health_status['checks']['redis'] = f'error: {str(e)}'
        
        status_code = 200 if health_status['status'] == 'healthy' else 503
        return Response(health_status, status=status_code)
