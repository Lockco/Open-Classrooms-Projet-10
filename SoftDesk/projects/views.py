from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.decorators import api_view


@api_view(['GET'])
def project_list(request):
    """ permet de récupérer la liste de tous les projets """
    if not request.user.is_authenticated:
        return Response({'message': 'Vous devez être connecté pour accéder à cette page'})
    projects = Project.objects.filter(author=request.user)
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)
