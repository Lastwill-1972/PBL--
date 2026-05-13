from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'location', 'start_time', 'end_time', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'content', 'location')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)