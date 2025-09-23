from django.contrib import admin
from .models import ScheduledPost

# Register your models here.

class ScheduledPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_content', 'scheduled_time', 'status', 'published_at')
    list_filter = ('status', 'scheduled_time')
    search_fields = ('text_content',)
    ordering = ('-scheduled_time',)
admin.site.register(ScheduledPost, ScheduledPostAdmin)


