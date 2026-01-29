from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via SMTP"""
    
    @staticmethod
    def send_email(to_email, subject, html_content, attachment_path=None):
        """
        Send email using Django's SMTP backend
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            attachment_path: Optional path to file attachment
        
        Returns:
            Boolean indicating success
        """
        try:
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email],
            )
            email.content_subtype = 'html'  # Send as HTML
            
            # Add attachment if provided
            if attachment_path:
                email.attach_file(attachment_path)
            
            email.send()
            
            logger.info(f"Email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False
    
    @staticmethod
    def send_auto_response(customer_email, customer_name):
        """Send automatic confirmation email to customer"""
        from .models import SystemSettings
        
        settings_obj = SystemSettings.load()
        
        if not settings_obj.auto_response_enabled:
            return False
        
        subject = "Message Received - We'll Be In Touch Soon"
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #4a90e2;">Hello {customer_name},</h2>
                    <p>{settings_obj.auto_response_message}</p>
                    <p>Our team will review your message and get back to you as soon as possible.</p>
                    <br>
                    <p style="color: #666; font-size: 0.9em;">
                        This is an automated message. Please do not reply to this email.
                    </p>
                </div>
            </body>
        </html>
        """
        
        return EmailService.send_email(customer_email, subject, html_content)
    
    @staticmethod
    def send_admin_notification(message_obj):
        """Notify admin of new message"""
        from .models import SystemSettings
        
        settings_obj = SystemSettings.load()
        
        if not settings_obj.admin_notification_enabled:
            return False
        
        subject = f"New Message: {message_obj.subject}"
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #4a90e2;">New Message Received</h2>
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>From:</strong></td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{message_obj.sender_name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Email:</strong></td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{message_obj.sender_email}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Subject:</strong></td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{message_obj.subject}</td>
                        </tr>
                        <tr>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;"><strong>Time:</strong></td>
                            <td style="padding: 10px; border-bottom: 1px solid #ddd;">{message_obj.timestamp}</td>
                        </tr>
                    </table>
                    <div style="margin-top: 20px; padding: 15px; background-color: #f5f5f5; border-left: 4px solid #4a90e2;">
                        <h3 style="margin-top: 0;">Message:</h3>
                        <p style="white-space: pre-wrap;">{message_obj.message_body}</p>
                    </div>
                    <p style="margin-top: 20px;">
                        <a href="http://localhost:8000/admin/helpdesk_app/message/{message_obj.id}/" 
                           style="background-color: #4a90e2; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            View in Admin Panel
                        </a>
                    </p>
                </div>
            </body>
        </html>
        """
        
        return EmailService.send_email(settings.ADMIN_EMAIL, subject, html_content)
    
    @staticmethod
    def send_reply_to_customer(message_obj, reply_obj):
        """Send admin's reply to customer"""
        subject = f"Re: {message_obj.subject}"
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #4a90e2;">Reply to Your Message</h2>
                    <p>Hello {message_obj.sender_name},</p>
                    <div style="margin-top: 20px; padding: 15px; background-color: #f5f5f5; border-left: 4px solid #4a90e2;">
                        <p style="white-space: pre-wrap;">{reply_obj.reply_body}</p>
                    </div>
                    <div style="margin-top: 30px; padding: 15px; background-color: #fafafa; border-top: 1px solid #ddd;">
                        <p style="color: #666; font-size: 0.9em; margin: 0;"><strong>Your Original Message:</strong></p>
                        <p style="color: #666; font-size: 0.9em; white-space: pre-wrap;">{message_obj.message_body}</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        return EmailService.send_email(message_obj.sender_email, subject, html_content)
