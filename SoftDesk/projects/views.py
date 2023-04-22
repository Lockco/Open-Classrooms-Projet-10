from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Project, Contributor
from .serializers import ProjectSerializer, ContributorSerializer
from users.models import User
from users.serializers import UserSerializer
from .permissions import IsProjectAuthorOrContributor

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


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
    permission_classes = [IsAuthenticated]
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
    Vue pour ajouter un utilisateur (collaborateur) à un projet existant.
    """
    serializer_class = ContributorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsProjectAuthorOrContributor]

    def create(self, request, *args, **kwargs):
        project_id = request.data.get('id')
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {'error': 'Project not found.'}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if the user is already a collaborator
        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND
            )
        if project.contributors.filter(user=user).exists():
            return Response(
                {'error': 'This user is already a collaborator on this project.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create a new contributor object and save it to the database
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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

