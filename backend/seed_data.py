"""
Seed script to populate database with sample data for testing
Run with: python manage.py shell < seed_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.core.settings')
django.setup()

from app.models import User, Task, Feedback
from datetime import datetime, timedelta

# Create test user
print("Creating test user...")
user, created = User.objects.get_or_create(
    email='test@example.com',
    defaults={'name': 'Test User'}
)
if created:
    user.set_password('password123')
    user.save()
    print("✓ Test user created (email: test@example.com, password: password123)")
else:
    print("✓ Test user already exists")

# Create sample tasks
print("\nCreating sample tasks...")
tasks_data = [
    {
        'title': 'Complete project documentation',
        'description': 'Write comprehensive documentation for the project',
        'priority': 'High',
        'status': 'Completed',
        'due_date': datetime.now().date() - timedelta(days=2)
    },
    {
        'title': 'Review pull requests',
        'description': 'Review and merge pending pull requests',
        'priority': 'Medium',
        'status': 'Completed',
        'due_date': datetime.now().date() - timedelta(days=1)
    },
    {
        'title': 'Update dependencies',
        'description': 'Update all project dependencies to latest versions',
        'priority': 'Low',
        'status': 'Pending',
        'due_date': datetime.now().date() + timedelta(days=7)
    },
    {
        'title': 'Fix critical bug',
        'description': 'Fix the authentication bug reported by users',
        'priority': 'High',
        'status': 'Pending',
        'due_date': datetime.now().date() + timedelta(days=1)
    },
    {
        'title': 'Implement new feature',
        'description': 'Add dark mode support to the application',
        'priority': 'Medium',
        'status': 'Pending',
        'due_date': datetime.now().date() + timedelta(days=14)
    },
    {
        'title': 'Write unit tests',
        'description': 'Increase test coverage to 80%',
        'priority': 'High',
        'status': 'Completed',
        'due_date': datetime.now().date() - timedelta(days=3)
    },
    {
        'title': 'Optimize database queries',
        'description': 'Improve performance of slow queries',
        'priority': 'Medium',
        'status': 'Pending',
        'due_date': datetime.now().date() + timedelta(days=10)
    },
    {
        'title': 'Update README',
        'description': 'Add setup instructions and examples',
        'priority': 'Low',
        'status': 'Completed',
        'due_date': datetime.now().date() - timedelta(days=5)
    },
]

for task_data in tasks_data:
    task, created = Task.objects.get_or_create(
        user=user,
        title=task_data['title'],
        defaults=task_data
    )
    if created:
        print(f"✓ Created task: {task.title}")

# Create sample feedback
print("\nCreating sample feedback...")
feedback_data = [
    {
        'comment': 'Great task management system! Very intuitive.',
        'rating': 5
    },
    {
        'comment': 'Would love to see more filtering options.',
        'rating': 4
    },
]

for fb_data in feedback_data:
    feedback, created = Feedback.objects.get_or_create(
        user=user,
        comment=fb_data['comment'],
        defaults=fb_data
    )
    if created:
        print(f"✓ Created feedback with rating: {feedback.rating}")

print("\n✅ Seed data created successfully!")
print("\nYou can now login with:")
print("Email: test@example.com")
print("Password: password123")
