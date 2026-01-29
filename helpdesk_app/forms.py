from django import forms
from .models import Message, Reply
import re


class MessageForm(forms.ModelForm):
    """Form for customer message submission"""
    
    class Meta:
        model = Message
        fields = ['sender_name', 'sender_email', 'subject', 'message_body', 'attachment']
        widgets = {
            'sender_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'sender_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject',
                'required': True
            }),
            'message_body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message...',
                'rows': 5,
                'required': True
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
    
    def clean_sender_name(self):
        name = self.cleaned_data.get('sender_name')
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        # Remove any HTML tags
        name = re.sub(r'<[^>]*>', '', name)
        return name
    
    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if len(subject) < 3:
            raise forms.ValidationError("Subject must be at least 3 characters long.")
        # Remove any HTML tags
        subject = re.sub(r'<[^>]*>', '', subject)
        return subject
    
    def clean_message_body(self):
        message = self.cleaned_data.get('message_body')
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters long.")
        # Remove any HTML tags
        message = re.sub(r'<[^>]*>', '', message)
        return message
    
    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        if attachment:
            # Limit file size to 5MB
            if attachment.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must not exceed 5MB.")
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.txt', '.jpg', '.jpeg', '.png']
            ext = attachment.name[attachment.name.rfind('.'):].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(f"Allowed file types: {', '.join(allowed_extensions)}")
        
        return attachment


class ReplyForm(forms.ModelForm):
    """Form for admin replies"""
    
    class Meta:
        model = Reply
        fields = ['reply_body']
        widgets = {
            'reply_body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your reply here...',
                'rows': 5,
                'required': True
            }),
        }
    
    def clean_reply_body(self):
        reply = self.cleaned_data.get('reply_body')
        if len(reply) < 10:
            raise forms.ValidationError("Reply must be at least 10 characters long.")
        return reply
