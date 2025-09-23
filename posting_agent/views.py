from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ScheduledPost
from .serializers import HashtagSuggestionSerializer, ScheduledPostSerializer
from .tasks import publish_post_task 
from .ai_utils import generate_hashtags 
from rest_framework.views import APIView
from django.shortcuts import render



class ScheduledPostViewSet(viewsets.ModelViewSet):

    queryset = ScheduledPost.objects.all()
    serializer_class = ScheduledPostSerializer
    
    # Task 1: Create/Submit Post
    def perform_create(self, serializer):
        post_instance = serializer.save(status='SCHEDULED')

        # Schedule the Celery task to publish the post at the scheduled_time
        publish_post_task.apply_async(
            args=[post_instance.id], 
            eta=post_instance.scheduled_time
        )
    
    # AI Helper to suggest hashtags [URL: /api/posts/suggest_hashtags/]
    @action(detail=False, methods=['post'])
    def suggest_hashtags(self, request):

        text = request.data.get('text_content')
        if not text:
            return Response(
                {"error": "Missing 'text_content' in request data."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call the actual Gemini helper function
        suggestions = generate_hashtags(text)
        
        return Response({
            "text_content": text,
            "suggested_hashtags": suggestions
        }, status=status.HTTP_200_OK)
    

#HashtagSuggestionAPIView
class HashtagSuggestionAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = HashtagSuggestionSerializer(data=request.data)
        if serializer.is_valid():
            text_content = serializer.validated_data['text_content']
            suggested_hashtags = generate_hashtags(text_content)
            return Response({
                "text_content": text_content,
                "suggested_hashtags": suggested_hashtags
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- API View for Dashboard Statistics ---

class DashboardStatsView(APIView):
    def get(self, request, *args, **kwargs):
        platform_filter = request.query_params.get('platform')
        queryset = ScheduledPost.objects.all()
        if platform_filter:
            queryset = queryset.filter(target_platforms__contains=[platform_filter])

        published_count = queryset.filter(status='PUBLISHED').count()
        scheduled_count = queryset.filter(status='SCHEDULED').count()
        failed_count = queryset.filter(status='FAILED').count()
        total_posts = queryset.count()
        
        data = {
            "total_posts": total_posts,
            "posts_published": published_count,
            "posts_scheduled": scheduled_count,
            "posts_failed": failed_count,
            "platform_filter": platform_filter,
            "platform_options": ["Facebook", "Twitter", "LinkedIn", "FAIL_PLATFORM"]
        }
        
        return Response(data, status=status.HTTP_200_OK)

class AIInsightView(APIView):
    def get(self, request, *args, **kwargs):
        platform_filter = request.query_params.get('platform')

        if platform_filter:
            # Filter posts for the specific platform
            published_on_platform = ScheduledPost.objects.filter(
                target_platforms__contains=[platform_filter],
                status='PUBLISHED'
            ).count()
            
            # Generate a specific insight for the platform
            if published_on_platform == 0:
                insight = f"No posts have been published to {platform_filter} yet. Start scheduling to see insights!"
            elif published_on_platform < 2:
                insight = f"Only {published_on_platform} posts published on {platform_filter}. Consider analyzing your target audience on this platform for better results."
            else:
                insight = f"You've had {published_on_platform} successful posts on {platform_filter}. This platform is performing well! Keep it up."
        else:
            # General insight for all platforms
            total_published = ScheduledPost.objects.filter(status='PUBLISHED').count()
            if total_published == 0:
                insight = "No posts have been published yet. Schedule your first post to start analyzing performance!"
            elif total_published < 5:
                insight = f"Only {total_published} posts published. Focusing on peak times could boost engagement."
            else:
                insight = "The current post success rate is excellent! Keep up the good work."

        return Response({"insight": insight}, status=status.HTTP_200_OK)
    
# --- Simple Dashboard View ---
def dashboard_view(request):
    return render(request, 'dashboard.html', {})