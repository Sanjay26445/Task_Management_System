from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, FeedbackViewSet, AnalyticsView
from .auth_views import RegisterView, LoginView, RefreshTokenView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'feedback', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('', include(router.urls)),
]
