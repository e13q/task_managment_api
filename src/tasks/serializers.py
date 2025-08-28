from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField, BooleanField

from .models import Task, TaskAssignee

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'api_last_ip')


class TaskAssigneeSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = PrimaryKeyRelatedField(source='user', queryset=User.objects.all(), write_only=True)

    class Meta:
        model = TaskAssignee
        fields = ('user_id', 'user', 'task_resolved')
        read_only_fields = ('user', 'task_resolved')


class TaskSerializer(ModelSerializer):
    assignees = TaskAssigneeSerializer(many=True)
    created_by = UserSerializer(read_only=True)
    is_completed = BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'deadline', 'priority',
            'assignees', 'created_by', 'created_at', 'is_completed'
        ]
        read_only_fields = ['created_by', 'created_at', 'is_completed']

    def create(self, validated_data):
        assignees = validated_data.pop('assignees', [])
        validated_data['created_by'] = self.context['request'].user
        task = Task.objects.create(**validated_data)
        for assignee in assignees:
            TaskAssignee.objects.create(task=task, **assignee)
        return task
