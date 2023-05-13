from django.contrib import admin

from .models import Tag, Change, Project, Task


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['user', 'title']
    search_fields = ['user__username', 'title']
    ordering = ['user', 'title']
    list_filter = ['user']


@admin.register(Change)
class ChangeAdmin(admin.ModelAdmin):
    list_display = ['user', 'table', 'data_id', 'action']
    search_fields = ['user__username', 'table', 'data_id', 'action']
    ordering = ['user', 'table', 'data_id', 'action']
    list_filter = ['user', 'table', 'action']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'deadline']
    search_fields = ['user__username', 'title', 'description', 'deadline']
    ordering = ['user', 'title', 'description', 'deadline']
    list_filter = ['user']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'deadline', 'duration', 'completed', 'occurrence', 'priority',
                    'reminder', 'project']
    search_fields = ['user__username', 'title', 'description', 'deadline', 'duration', 'completed', 'occurrence',
                     'priority', 'reminder', 'project__title', 'tags__title']
    ordering = ['user', 'title', 'description', 'deadline', 'duration', 'completed', 'occurrence', 'priority',
                'reminder', 'project', 'tags']
    list_filter = ['user', 'completed', 'priority', 'reminder', 'project', 'tags']
