from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from users.models import User
from users.serializers import UserSerializer
from .permissions import IsProjectAuthorOrContributor, IsIssueAuthorOrReadOnly, IsCommentAuthorOrReadOnly

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


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


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsIssueAuthorOrReadOnly]

    def perform_create(self, serializer):
        project_id = self.kwargs['project_pk']  # Récupérer l'ID du projet depuis les données de la requête
        project = get_object_or_404(Project, id=project_id)
        serializer.save(author=self.request.user, project=project)  # Spécifier l'ID du projet lors de la sauvegarde de l'issue

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthorOrReadOnly]

    def perform_create(self, serializer):
        issue_id = self.kwargs['issue_pk']
        issue = get_object_or_404(Issue, id=issue_id)
        serializer.save(author=self.request.user, issue=issue)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectAuthorOrContributor]

    def create(self, request, *args, **kwargs):
        data_copy = request.data.copy()
        username = data_copy.get("user")
        user = get_object_or_404(User, username=username)
        data_copy["user"] = user.id
        serializer = ContributorSerializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
