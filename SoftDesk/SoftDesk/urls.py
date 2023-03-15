from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', schema_view),
    path('docs-coreapi/', include_docs_urls(title='API Documentation')),
    path('', include('projects.urls')),
    path('', include('users.urls')),
]