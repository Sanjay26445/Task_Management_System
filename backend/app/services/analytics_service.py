from django.db.models import Count, Avg, Q, F
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from app.models import Task


class AnalyticsService:
    @staticmethod
    def get_user_analytics(user):
        """Calculate comprehensive analytics for a user"""
        tasks = Task.objects.filter(user=user)
        
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='Completed').count()
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Tasks per day
        tasks_per_day = list(
            tasks.filter(status='Completed')
            .annotate(date=TruncDate('updated_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )
        
        # Most productive day
        most_productive_day = None
        if tasks_per_day:
            most_productive = max(tasks_per_day, key=lambda x: x['count'])
            most_productive_day = {
                'date': most_productive['date'].strftime('%Y-%m-%d'),
                'count': most_productive['count']
            }
        
        # Average completion time
        completed = tasks.filter(status='Completed')
        avg_completion_time = None
        if completed.exists():
            total_time = timedelta()
            count = 0
            for task in completed:
                time_diff = task.updated_at - task.created_at
                total_time += time_diff
                count += 1
            avg_seconds = total_time.total_seconds() / count
            avg_completion_time = avg_seconds / 3600  # Convert to hours
        
        # Priority distribution
        priority_distribution = {
            'Low': tasks.filter(priority='Low').count(),
            'Medium': tasks.filter(priority='Medium').count(),
            'High': tasks.filter(priority='High').count(),
        }
        
        # Productivity score
        productivity_score = AnalyticsService._calculate_productivity_score(user, tasks)
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_percentage': round(completion_percentage, 2),
            'tasks_per_day': tasks_per_day,
            'most_productive_day': most_productive_day,
            'average_completion_time_hours': round(avg_completion_time, 2) if avg_completion_time else None,
            'priority_distribution': priority_distribution,
            'productivity_score': round(productivity_score, 2)
        }
    
    @staticmethod
    def _calculate_productivity_score(user, tasks):
        """
        Calculate productivity score based on:
        - Completed tasks (10 points each)
        - High priority completed (5 bonus points)
        - Medium priority completed (3 bonus points)
        - On-time completions (7 bonus points)
        - Overdue tasks (3 penalty points)
        Normalized by days active
        """
        completed = tasks.filter(status='Completed')
        completed_count = completed.count()
        
        high_priority_completed = completed.filter(priority='High').count()
        medium_priority_completed = completed.filter(priority='Medium').count()
        
        # On-time completions (completed before due date)
        on_time = completed.filter(
            Q(due_date__isnull=False) & Q(updated_at__date__lte=F('due_date'))
        ).count()
        
        # Overdue tasks
        today = datetime.now().date()
        overdue = tasks.filter(
            Q(status='Pending') & Q(due_date__isnull=False) & Q(due_date__lt=today)
        ).count()
        
        # Calculate days active
        if tasks.exists():
            first_task = tasks.order_by('created_at').first()
            days_active = (datetime.now().date() - first_task.created_at.date()).days + 1
        else:
            days_active = 1
        
        score = (
            (completed_count * 10) +
            (high_priority_completed * 5) +
            (medium_priority_completed * 3) +
            (on_time * 7) -
            (overdue * 3)
        ) / days_active
        
        return max(score, 0)  # Ensure non-negative
