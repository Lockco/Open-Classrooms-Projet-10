from rest_framework import permissions


class IsProjectAuthorOrContributor(permissions.BasePermission):
    """
     Permission personnalisée pour vérifier si l'utilisateur est l'auteur du projet ou un contributeur.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if obj.author == request.user or request.user in obj.contributors.all():
                return True
        return False


class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour autoriser uniquement les auteurs des commentaires à les modifier ou à les supprimer.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsIssueAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour autoriser uniquement les auteurs des problèmes à les modifier ou à les supprimer.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
