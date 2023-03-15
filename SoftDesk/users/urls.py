from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserViewSet, signup, obtain_token, login_user
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration de la documentation
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
    ),
    public=True,
)

# Configuration des routes de l'API
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# Configuration des URL
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework_V1')),
    path('signup/', signup, name='signup'),
    path('login/', login_user, name='login'),
    # path('obtain_token/', obtain_auth_token, name='api_token_auth'),
    path('obtain_token/', obtain_token, name='obtain_token'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += router.urls
