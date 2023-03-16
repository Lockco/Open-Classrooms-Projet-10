from rest_framework import status, viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
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
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def obtain_token(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = authenticate(username=username, password=password)

#     if user is None:
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

#     serializer = UserSerializer(user)

#     refresh = RefreshToken.for_user(user)

#     return Response({
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#         'user': serializer.data,
#     }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_authenticated(request):
    """
    Endpoint pour tester si un utilisateur est connecté.
    """
    return Response({"message": "Vous êtes connecté !"})