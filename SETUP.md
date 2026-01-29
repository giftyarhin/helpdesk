# Interactive Single-Endpoint Emailing System - Setup Guide

This is a Django-based helpdesk system where all customer messages are routed to a single admin inbox.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL Server
- SendGrid Account (for email service)

### Installation Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd /Users/alorzigy/Desktop/helpdesk
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL Database**
   ```bash
   # Log into MySQL
   mysql -u root -p
   
   # Create database
   CREATE DATABASE helpdesk_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   
   # Create user (optional)
   CREATE USER 'helpdesk_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON helpdesk_db.* TO 'helpdesk_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

5. **Configure Environment Variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your actual values
   nano .env
   ```
   
   Update these values in `.env`:
   - `SECRET_KEY`: Generate a secure secret key
   - `DB_PASSWORD`: Your MySQL password
   - `SENDGRID_API_KEY`: Your SendGrid API key
   - `SENDGRID_FROM_EMAIL`: Your verified sender email
   - `ADMIN_EMAIL`: Email where notifications will be sent

6. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create Admin User**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin account.

8. **Create Static and Media Directories**
   ```bash
   mkdir -p static media
   ```

9. **Collect Static Files**
   ```bash
   python manage.py collectstatic --noinput
   ```

10. **Run the Development Server**
    ```bash
    python manage.py runserver
    ```
    
    Access the application at: http://localhost:8000

## 📧 SendGrid Configuration

1. Sign up for a free SendGrid account at https://sendgrid.com
2. Create an API Key with "Mail Send" permissions
3. Verify your sender email address in SendGrid
4. Add the API key and sender email to your `.env` file

## 🎯 Features

### Customer Features
- Submit messages via web form
- Automatic confirmation email
- File attachment support (up to 5MB)
- Rate limiting (5 messages per hour per IP)

### Admin Features
- Secure login to admin panel
- Unified inbox for all messages
- Search and filter messages
- Reply to customers via email
- Message status tracking (New/Replied)
- View message history and threads

## 🔒 Security Features

- CSRF protection
- XSS prevention (input sanitization)
- Rate limiting on contact form
- Secure session management
- HTTPS ready
- Security headers middleware
- File upload validation

## 📁 Project Structure

```
helpdesk/
├── helpdesk/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── helpdesk_app/          # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Form definitions
│   ├── admin.py           # Admin configuration
│   ├── email_service.py   # Email functionality
│   ├── middleware.py      # Custom middleware
│   └── urls.py            # URL routing
├── templates/             # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── contact.html
│   ├── inbox.html
│   ├── message_detail.html
│   └── login.html
├── static/                # Static files (CSS/JS)
├── media/                 # User uploads
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## 🗄️ Database Schema

### Message Model
- sender_name
- sender_email
- subject
- message_body
- timestamp
- status (new/replied)
- attachment (optional)

### Reply Model
- message (ForeignKey)
- admin (ForeignKey to User)
- reply_body
- timestamp

### SystemSettings Model
- auto_response_enabled
- auto_response_message
- admin_notification_enabled

## 🌐 URLs

- `/` - Homepage
- `/contact/` - Contact form (public)
- `/login/` - Admin login
- `/inbox/` - Admin inbox (requires login)
- `/message/<id>/` - Message detail and reply (requires login)
- `/admin/` - Django admin panel

## 🧪 Running Tests

```bash
python manage.py test helpdesk_app
```

## 📊 Admin Panel

Access the Django admin panel at http://localhost:8000/admin/

Features:
- Manage messages and replies
- Configure system settings
- View analytics
- User management

## 🚀 Production Deployment

### Important Settings for Production

1. Set `DEBUG=False` in `.env`
2. Update `ALLOWED_HOSTS` with your domain
3. Use a strong `SECRET_KEY`
4. Configure proper database credentials
5. Set up HTTPS (SSL certificate)
6. Configure static file serving (use Nginx or similar)
7. Set up proper logging
8. Enable email backend for production

### Recommended Production Setup

- **Web Server**: Nginx or Apache
- **Application Server**: Gunicorn or uWSGI
- **Database**: MySQL or PostgreSQL
- **Cache**: Redis or Memcached
- **Email**: SendGrid (configured)
- **Storage**: AWS S3 for media files (optional)

### Example Gunicorn Command

```bash
gunicorn helpdesk.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | `your-secret-key-here` |
| DEBUG | Debug mode | `False` |
| ALLOWED_HOSTS | Allowed domains | `yourdomain.com,www.yourdomain.com` |
| DB_NAME | Database name | `helpdesk_db` |
| DB_USER | Database user | `root` |
| DB_PASSWORD | Database password | `your-password` |
| DB_HOST | Database host | `localhost` |
| DB_PORT | Database port | `3306` |
| SENDGRID_API_KEY | SendGrid API key | `SG.xxxxx` |
| SENDGRID_FROM_EMAIL | Sender email | `noreply@yourdomain.com` |
| ADMIN_EMAIL | Admin notification email | `admin@yourdomain.com` |

## 🛠️ Troubleshooting

### Database Connection Issues
- Verify MySQL is running: `mysql.server status`
- Check credentials in `.env`
- Ensure database exists

### Email Not Sending
- Verify SendGrid API key is valid
- Check sender email is verified in SendGrid
- Review Django logs for errors

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check STATIC_ROOT and STATIC_URL settings
- Verify file permissions

## 📞 Support

For issues or questions, please check the main README.md or contact the development team.

## 📄 License

See LICENSE file for details.
