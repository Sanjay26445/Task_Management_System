from rest_framework import serializers
from app.models import Task, TaskHistory


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'status', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_priority(self, value):
        if value not in ['Low', 'Medium', 'High']:
            raise serializers.ValidationError("Priority must be Low, Medium, or High")
        return value

    def validate_status(self, value):
        if value not in ['Pending', 'Completed', 'Archived']:
            raise serializers.ValidationError("Status must be Pending, Completed, or Archived")
        return value


class TaskHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskHistory
        fields = ['id', 'action_type', 'previous_state', 'timestamp']
        read_only_fields = ['id', 'timestamp']
