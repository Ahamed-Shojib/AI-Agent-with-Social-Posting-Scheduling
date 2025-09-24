# social_scheduler/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from posting_agent.views import ScheduledPostViewSet
from posting_agent.views import DashboardStatsView, AIInsightView 
from posting_agent.views import dashboard_view, HashtagSuggestionAPIView
# Initialize DRF Router
router = DefaultRouter()
router.register(r'posts', ScheduledPostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), # Exposes /api/posts/ and /api/posts/suggest_hashtags/

    #Dashboard Pages URL
    path('', dashboard_view, name='dashboard-page'),
    path('api/dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('api/dashboard/insight/', AIInsightView.as_view(), name='ai-insight'),
    path('api/posts/hashtags/', HashtagSuggestionAPIView.as_view(), name='hashtag-suggestion'),
   
    #Task_2 URL
    path('task2/', include('task_2.urls')),
]

# Serve media files (images) only during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

