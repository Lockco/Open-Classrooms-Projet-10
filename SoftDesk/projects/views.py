from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Project
from .serializers import ProjectSerializer


class ProjectCreateView(generics.CreateAPIView):
    """
    Vue pour créer un nouveau projet.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
