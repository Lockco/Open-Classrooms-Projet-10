from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, User
import logging

logger = logging.getLogger(__name__)


class UserCreate(generics.CreateAPIView):
    """
    Vue pour créer un nouvel utilisateur.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]  # autoriser les utilisateurs non authentifiés à s'inscrire
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Vue permet aux utilisateurs d'être affichés ou modifiés.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]