from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Project
from .serializers import ProjectSerializer
from users.models import User
from users.serializers import UserSerializer

User = get_user_model()


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


class ProjectListView(generics.ListAPIView):
    """
    Récupère la liste de tous les projets rattachés à l'utilisateur connecté
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)


class ProjectDetail(generics.RetrieveAPIView):
    """
    Récupère les détails d'un projet par son id.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


class ProjectUpdateView(generics.UpdateAPIView):
    """
    Vue pour mettre à jour un projet.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    allowed_methods = ['PUT', 'PATCH', 'OPTIONS']

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class ProjectDeleteView(generics.DestroyAPIView):
    """
    Vue pour supprimer un projet.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Le projet a été supprimé avec succès."})


class ProjectAddUserView(generics.CreateAPIView):
    """
    Vue pour ajouter un utilisateur (collaborateur) à un projet.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND
            )
        if project.author != request.user and user != request.user:
            return Response(
                {'error': 'You do not have permission to add this user to the project.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        if user in project.users.all():
            return Response(
                {'error': 'This user is already a collaborator on this project.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        project.users.add(user)
        project.save()
        serializer = self.serializer_class(project)
        return Response(serializer.data)


class ProjectUsersListView(generics.ListAPIView):
    """
    Vue pour récupérer la liste de tous les utilisateurs attachés à un projet.
    """
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs['pk']
        project = get_object_or_404(Project, id=project_id)
        users_ids = project.contributors.values_list('user_id', flat=True)
        return User.objects.filter(id__in=users_ids)
