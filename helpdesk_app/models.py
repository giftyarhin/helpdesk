from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Message(models.Model):
    """Model for customer messages"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('replied', 'Replied'),
    ]
    
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=300)
    message_body = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['status']),
            models.Index(fields=['sender_email']),
        ]
    
    def __str__(self):
        return f"{self.sender_name} - {self.subject}"


class Reply(models.Model):
    """Model for admin replies to customer messages"""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='replies')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply_body = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Replies'
    
    def __str__(self):
        return f"Reply to {self.message.subject}"


class SystemSettings(models.Model):
    """Model for system configuration"""
    auto_response_enabled = models.BooleanField(default=True)
    auto_response_message = models.TextField(
        default="Thank you for contacting us. We have received your message and will respond shortly."
    )
    admin_notification_enabled = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'System Settings'
        verbose_name_plural = 'System Settings'
    
    def __str__(self):
        return "System Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
