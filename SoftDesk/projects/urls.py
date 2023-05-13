# from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
# from .views import ProjectCreateView, ProjectListView, ProjectDetail, ProjectUpdateView, ProjectDeleteView, \
#     ProjectAddUserView, ProjectUsersListView
#
# # urlpatterns = format_suffix_patterns(urlpatterns)
#
# urlpatterns = [
#
#     path('projects/', ProjectCreateView.as_view(), name='projects'),
#     path('projects/list/', ProjectListView.as_view(), name='projects-list'),
#     path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
#     path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
#     path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
#     path('projects/<int:pk>/users/', ProjectAddUserView.as_view(), name='project-add-user'),
#     path('projects/<int:pk>/users/list', ProjectUsersListView.as_view(), name='project-user-list'),
#     # path('projects/<int:pk>/issues/', IssueList.as_view(), name='issue-list'),
#     # path('projects/<int:project_pk>/issues/<int:pk>/', IssueDetail.as_view(), name='issue-detail'),
#     # path('projects/<int:project_pk>/issues/<int:pk>/comments/', CommentList.as_view(), name='comment-list'),
#     # path('projects/<int:project_pk>/issues/<int:issue_pk>/comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
# ]

from django.urls import include, path
from rest_framework_nested import routers
from .views import ProjectViewSet, IssueViewSet, CommentViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.documentation import include_docs_urls

router = routers.SimpleRouter()
router.register(r'projects', ProjectViewSet)

# Création d'un routeur imbriqué pour les problèmes (issues)
issue_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
issue_router.register(r'issues', IssueViewSet, basename='project-issues')

# Création d'un routeur imbriqué pour les commentaires
comment_router = routers.NestedSimpleRouter(issue_router, r'issues', lookup='issue')
comment_router.register(r'comments', CommentViewSet, basename='issue-comments')

# Configuration de la documentation Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for SoftDesk project"
    ),
    public=True,
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(issue_router.urls)),
    path('', include(comment_router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs-coreapi/', include_docs_urls(title='API Documentation')),
]
