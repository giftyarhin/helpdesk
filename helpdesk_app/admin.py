from django.contrib import admin
from .models import Message, Reply, SystemSettings


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'sender_email', 'subject', 'timestamp', 'status']
    list_filter = ['status', 'timestamp']
    search_fields = ['sender_name', 'sender_email', 'subject', 'message_body']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('sender_name', 'sender_email')
        }),
        ('Message Details', {
            'fields': ('subject', 'message_body', 'attachment')
        }),
        ('Status', {
            'fields': ('status', 'timestamp')
        }),
    )


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ['message', 'admin', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['message__subject', 'reply_body']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Prevent adding multiple instances
        return not SystemSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deleting the settings
        return False
