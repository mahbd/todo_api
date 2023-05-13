from django.contrib import admin

from .models import Tag, Change, Project, Task, Shared


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'user']
    search_fields = ['user__username', 'title']
    list_filter = ['user', 'created_at']


@admin.register(Change)
class ChangeAdmin(admin.ModelAdmin):
    list_display = ['user', 'table', 'data_id', 'action']
    search_fields = ['user__username', 'table', 'data_id', 'action']
    list_filter = ['user', 'table', 'action', 'created_at']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'user', 'description', 'deadline']
    search_fields = ['user__username', 'title', 'description', 'deadline']
    list_filter = ['user', 'created_at', 'deadline']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'description', 'deadline', 'duration', 'completed', 'occurrence', 'priority',
                    'reminder', 'project']
    search_fields = ['user__username', 'title', 'description', 'project__title', 'tags__title']
    list_filter = ['user', 'completed', 'priority', 'project', 'tags', 'created_at']


@admin.register(Shared)
class SharedAdmin(admin.ModelAdmin):
    list_display = ['user', 'shared_with', 'table', 'title']
    search_fields = ['user__username', 'shared_with__username']
    list_filter = ['user', 'shared_with', 'created_at']

    def title(self, obj: Shared):
        if obj.table == Shared.SHARED_TAG:
            return Tag.objects.get(id=obj.data_id).title
        elif obj.table == Shared.SHARED_PROJECT:
            return Project.objects.get(id=obj.data_id).title
