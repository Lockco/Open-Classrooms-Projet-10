from django.urls import path
from .views import UserCreate, UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('users/register/', UserCreate.as_view(), name='user-register'),
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
]