from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ProjectCreateView


# urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns = [

    path('projects/', ProjectCreateView.as_view(), name='projects')
    # path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    # path('projects/<int:pk>/users/', ProjectUserList.as_view(), name='project-user-list'),
    # path('projects/<int:pk>/issues/', IssueList.as_view(), name='issue-list'),
    # path('projects/<int:project_pk>/issues/<int:pk>/', IssueDetail.as_view(), name='issue-detail'),
    # path('projects/<int:project_pk>/issues/<int:pk>/comments/', CommentList.as_view(), name='comment-list'),
    # path('projects/<int:project_pk>/issues/<int:issue_pk>/comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
]


