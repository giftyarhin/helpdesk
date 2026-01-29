from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
from .models import Message, Reply
from .forms import MessageForm, ReplyForm
from .email_service import EmailService
import logging

logger = logging.getLogger(__name__)


@ratelimit(key='ip', rate='5/h', method='POST')
def contact_view(request):
    """Public contact form for customers to submit messages"""
    was_limited = getattr(request, 'limited', False)
    
    if was_limited:
        messages.error(request, 'Too many requests. Please try again later.')
        return render(request, 'contact.html', {'form': MessageForm()})
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Save the message
                message = form.save()
                
                # Send auto-response to customer
                EmailService.send_auto_response(
                    message.sender_email,
                    message.sender_name
                )
                
                # Notify admin
                EmailService.send_admin_notification(message)
                
                messages.success(
                    request,
                    'Thank you for your message! We will get back to you soon.'
                )
                return redirect('contact')
                
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                messages.error(
                    request,
                    'An error occurred while sending your message. Please try again.'
                )
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MessageForm()
    
    return render(request, 'contact.html', {'form': form})


@login_required
def inbox_view(request):
    """Admin inbox view showing all messages"""
    # Get search and filter parameters
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    
    # Base queryset
    messages_list = Message.objects.all()
    
    # Apply search
    if search_query:
        messages_list = messages_list.filter(
            Q(sender_name__icontains=search_query) |
            Q(sender_email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message_body__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter:
        messages_list = messages_list.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(messages_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_messages': messages_list.count(),
        'new_messages': Message.objects.filter(status='new').count(),
    }
    
    return render(request, 'inbox.html', context)


@login_required
def message_detail_view(request, message_id):
    """View and reply to a specific message"""
    message = get_object_or_404(Message, id=message_id)
    replies = message.replies.all()
    
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            try:
                # Save the reply
                reply = form.save(commit=False)
                reply.message = message
                reply.admin = request.user
                reply.save()
                
                # Update message status
                message.status = 'replied'
                message.save()
                
                # Send reply to customer
                EmailService.send_reply_to_customer(message, reply)
                
                messages.success(request, 'Reply sent successfully!')
                return redirect('message_detail', message_id=message.id)
                
            except Exception as e:
                logger.error(f"Error sending reply: {str(e)}")
                messages.error(request, 'Error sending reply. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReplyForm()
    
    context = {
        'message': message,
        'replies': replies,
        'form': form,
    }
    
    return render(request, 'message_detail.html', context)


@login_required
def mark_as_read(request, message_id):
    """Mark a message as replied (manual status update)"""
    if request.method == 'POST':
        message = get_object_or_404(Message, id=message_id)
        message.status = 'replied'
        message.save()
        messages.success(request, 'Message marked as replied.')
    
    return redirect('inbox')


def home_view(request):
    """Homepage view"""
    return render(request, 'home.html')
