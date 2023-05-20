from rest_framework import serializers

from .models import Tag, Change, Project, Task, Shared


class TagSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Tag
        fields = ['id', 'user', 'title']
        read_only_fields = ['id']


class ChangeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Change
        fields = ['id', 'user', 'table', 'data_id', 'action']
        read_only_fields = ['id']


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ['id', 'user', 'title', 'description', 'deadline']
        read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    project = serializers.CharField(write_only=True, required=False, max_length=1023)
    tags = serializers.CharField(write_only=True, required=False, max_length=1023)
    tag_titles = serializers.SerializerMethodField()
    project_title = serializers.SerializerMethodField()

    def get_tag_titles(self, obj: Task):
        return [tag.title for tag in obj.tags.all()]

    def get_project_title(self, obj: Task):
        return obj.project.title if obj.project else ""

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'deadline', 'duration', 'completed', 'occurrence', 'priority',
                  'reminder', 'project', 'tags', 'project_title', 'tag_titles']
        read_only_fields = ['id', 'user']

    def validate(self, attrs: dict):
        user = self.context['request'].user
        tag_titles = attrs.pop('tags', "").split(", ") if attrs.get('tags', None) else []
        tags = []
        project_title = attrs.pop('project', None)
        for title in tag_titles:
            tag, _ = Tag.objects.get_or_create(title=title, user=user)
            tags.append(tag)
        attrs['tags'] = tags
        if project_title:
            project, _ = Project.objects.get_or_create(title=project_title, user=user)
            attrs['project'] = project
        attrs['user'] = user
        return attrs


class SharedSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    title = serializers.SerializerMethodField()

    def get_title(self, obj: Shared):
        if obj.table == Shared.SHARED_TAG:
            return Tag.objects.get(id=obj.data_id).title
        elif obj.table == Shared.SHARED_PROJECT:
            return Project.objects.get(id=obj.data_id).title

    class Meta:
        model = Shared
        fields = ['id', 'user', 'table', 'shared_with', 'data_id', 'title']
        read_only_fields = ['id', 'user']

    def validate(self, attrs: dict):
        attrs['user'] = self.context['request'].user
        return attrs
