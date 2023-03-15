from django.contrib import admin

from .models import Project, Issue, Comment, Contributor


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'type', 'author')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'priority', 'project', 'status', 'author', 'assignee', 'created_time', 'tags')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('description', 'author', 'issue', 'created_time')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'permission', 'role')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Contributor, ContributorAdmin)
