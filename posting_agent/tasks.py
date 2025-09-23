import logging
import time
from celery import shared_task
from django.utils import timezone
from .models import ScheduledPost

logger = logging.getLogger(__name__)

# --- Mock Social Media Posting Functions ---
def mock_publish(platform, text, image_path):
    # Simulate network latency
    time.sleep(1) 
    
    # Simulate a failure for a specific platform
    if 'FAIL' in platform.upper():
        logger.error(f"Mock API Error: Failed to publish to {platform}")
        return False
        
    logger.info(f"Successfully published to {platform} using image: {image_path}")
    return True

@shared_task
def publish_post_task(post_id):
    logger.info(f"Starting publish_post_task for Post ID: {post_id}")
    try:
        post = ScheduledPost.objects.get(id=post_id)
        
        if post.status != 'SCHEDULED':
            logger.warning(f"Post ID {post_id} is not SCHEDULED. Status: {post.status}. Aborting.")
            return

        post.status = 'PUBLISHING'
        post.save()
    except ScheduledPost.DoesNotExist:
        logger.error(f"Post ID {post_id} not found.")
        return

    all_successful = True
    image_path = post.image.path 

    for platform in post.target_platforms:
        success = mock_publish(platform, post.text_content, image_path)
        if not success:
            all_successful = False

    # Update final status
    if all_successful:
        post.status = 'PUBLISHED'
        post.published_at = timezone.now()
    else:
        post.status = 'FAILED'
        
    post.save()
    logger.info(f"Post ID {post_id} final status: {post.status}")