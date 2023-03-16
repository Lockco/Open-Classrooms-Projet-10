from django.urls import path, include, re_path
from rest_framework import routers
from .views import UserViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import UserCreate
from rest_framework_simplejwt.views import TokenObtainPairView

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
    path('signup/', UserCreate.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('test/', test_authenticated, name='test_authenticated'),
    # path('obtain_token/', obtain_token, name='obtain_token'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework_V1')),
    # path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += router.urls
