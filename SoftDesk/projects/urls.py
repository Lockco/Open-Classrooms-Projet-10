from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ProjectCreateView, ProjectListView, ProjectDetail, ProjectUpdateView, ProjectDeleteView, \
    ProjectAddUserView, ProjectUsersListView

# urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns = [

    path('projects/', ProjectCreateView.as_view(), name='projects'),
    path('projects/list/', ProjectListView.as_view(), name='projects-list'),
    path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('projects/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('projects/<int:pk>/users/', ProjectAddUserView.as_view(), name='project-user-list'),
    path('projects/<int:pk>/users/list', ProjectUsersListView.as_view(), name='project-user-list'),
    # path('projects/<int:pk>/issues/', IssueList.as_view(), name='issue-list'),
    # path('projects/<int:project_pk>/issues/<int:pk>/', IssueDetail.as_view(), name='issue-detail'),
    # path('projects/<int:project_pk>/issues/<int:pk>/comments/', CommentList.as_view(), name='comment-list'),
    # path('projects/<int:project_pk>/issues/<int:issue_pk>/comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
]


