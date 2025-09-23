from django.db import models
from django.utils import timezone

class ScheduledPost(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SCHEDULED', 'Scheduled'),
        ('PUBLISHING', 'Publishing'),
        ('PUBLISHED', 'Published'),
        ('FAILED', 'Failed'),
    )

    text_content = models.TextField()
    image = models.ImageField(upload_to='post_images/') 
    
    scheduled_time = models.DateTimeField(db_index=True)
    target_platforms = models.JSONField(default=list) 
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['scheduled_time']

    def __str__(self):
        return f"Post ID {self.id} for {self.scheduled_time.strftime('%Y-%m-%d %H:%M')}"