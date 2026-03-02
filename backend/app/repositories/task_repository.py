from django.db.models import Q, Count, Avg, F
from datetime import datetime, timedelta
from app.models import Task, TaskHistory


class TaskRepository:
    @staticmethod
    def get_user_tasks(user, filters=None):
        """Get tasks for a user with optional filters"""
        queryset = Task.objects.filter(user=user)
        
        if filters:
            if 'status' in filters:
                queryset = queryset.filter(status=filters['status'])
            if 'priority' in filters:
                queryset = queryset.filter(priority=filters['priority'])
            if 'due_date' in filters:
                queryset = queryset.filter(due_date=filters['due_date'])
        
        return queryset

    @staticmethod
    def create_task(user, data):
        """Create a new task"""
        task = Task.objects.create(user=user, **data)
        TaskHistory.objects.create(
            task=task,
            action_type='created',
            previous_state=None
        )
        return task

    @staticmethod
    def update_task(task, data):
        """Update a task and record history"""
        previous_state = {
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'due_date': str(task.due_date) if task.due_date else None
        }
        
        for key, value in data.items():
            setattr(task, key, value)
        task.save()
        
        TaskHistory.objects.create(
            task=task,
            action_type='updated',
            previous_state=previous_state
        )
        return task

    @staticmethod
    def complete_task(task):
        """Mark task as completed"""
        previous_state = {'status': task.status}
        task.status = 'Completed'
        task.save()
        
        TaskHistory.objects.create(
            task=task,
            action_type='completed',
            previous_state=previous_state
        )
        return task

    @staticmethod
    def delete_task(task):
        """Delete task and record history"""
        previous_state = {
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'due_date': str(task.due_date) if task.due_date else None
        }
        
        TaskHistory.objects.create(
            task=task,
            action_type='deleted',
            previous_state=previous_state
        )
        task.delete()
