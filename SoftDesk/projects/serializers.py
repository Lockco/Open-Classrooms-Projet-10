from rest_framework import serializers
from .models import Project, Issue, Comment, Contributor
from users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'type', 'author')


class IssueSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    author = UserSerializer(read_only=True)
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = Issue
        fields = ('id', 'title', 'description', 'priority', 'project', 'status', 'author', 'assignee', 'created_time', 'tags')


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    issue = IssueSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'description', 'author', 'issue', 'created_time')


class ContributorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Contributor
        fields = ('id', 'user', 'project', 'permission', 'role')
