from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from app.models import Task, Feedback
from app.serializers.task import TaskSerializer
from app.serializers.feedback import FeedbackSerializer
from app.repositories.task_repository import TaskRepository
from app.services.analytics_service import AnalyticsService


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        filters = {}
        
        # Apply filters from query params
        status_filter = self.request.query_params.get('status')
        priority_filter = self.request.query_params.get('priority')
        due_date_filter = self.request.query_params.get('due_date')
        
        if status_filter:
            filters['status'] = status_filter
        if priority_filter:
            filters['priority'] = priority_filter
        if due_date_filter:
            filters['due_date'] = due_date_filter
        
        return TaskRepository.get_user_tasks(user, filters)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            task = TaskRepository.create_task(request.user, serializer.validated_data)
            return Response(
                TaskSerializer(task).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            task = self.get_queryset().get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {'error': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(data=request.data, partial=True)
        if serializer.is_valid():
            task = TaskRepository.update_task(task, serializer.validated_data)
            return Response(TaskSerializer(task).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            task = self.get_queryset().get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {'error': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        TaskRepository.delete_task(task)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        try:
            task = self.get_queryset().get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {'error': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        task = TaskRepository.complete_task(task)
        return Response(TaskSerializer(task).data)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        try:
            task = self.get_queryset().get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {'error': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        task = TaskRepository.update_task(task, {'status': 'Archived'})
        return Response(TaskSerializer(task).data)


class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        analytics = AnalyticsService.get_user_analytics(request.user)
        return Response(analytics)
