from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import project_list

urlpatterns = [
    # Autres URL
    path('projects/', project_list, name='project-list'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# urlpatterns = [

#     path('projects/<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
#     path('projects/<int:pk>/users/', ProjectUserList.as_view(), name='project-user-list'),
#     path('projects/<int:pk>/issues/', IssueList.as_view(), name='issue-list'),
#     path('projects/<int:project_pk>/issues/<int:pk>/', IssueDetail.as_view(), name='issue-detail'),
#     path('projects/<int:project_pk>/issues/<int:pk>/comments/', CommentList.as_view(), name='comment-list'),
#     path('projects/<int:project_pk>/issues/<int:issue_pk>/comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
# ]


