# Deployment Guide

Your helpdesk application is now ready to be deployed! Follow these steps:

## Option 1: Deploy to Render (Recommended - Free Tier Available)

1. **Sign up for Render**
   - Go to https://render.com
   - Sign up with your GitHub account

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `giftyarhin/helpdesk`
   - Render will automatically detect the `render.yaml` file

3. **Configure Environment Variables**
   - Render will auto-generate `SECRET_KEY`
   - Add these environment variables:
     ```
     DEBUG=False
     ALLOWED_HOSTS=your-app-name.onrender.com
     EMAIL_HOST_USER=your-email@gmail.com
     EMAIL_HOST_PASSWORD=your-app-password
     ```

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy your app automatically
   - Your app will be live at: `https://your-app-name.onrender.com`

## Option 2: Deploy to Railway

1. **Sign up for Railway**
   - Go to https://railway.app
   - Sign up with GitHub

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `giftyarhin/helpdesk`

3. **Add MySQL Database**
   - Click "New" → "Database" → "MySQL"
   - Railway will auto-configure `DATABASE_URL`

4. **Set Environment Variables**
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-app.railway.app
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

5. **Deploy**
   - Railway will automatically deploy
   - Access at your Railway domain

## Option 3: Deploy to PythonAnywhere

1. **Sign up**
   - Go to https://www.pythonanywhere.com
   - Create a free account

2. **Clone Repository**
   - Open a Bash console
   - Run: `git clone https://github.com/giftyarhin/helpdesk.git`

3. **Set up Virtual Environment**
   ```bash
   cd helpdesk
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Add a new web app
   - Choose "Manual configuration" with Python 3.10
   - Set source code directory to `/home/yourusername/helpdesk`
   - Set working directory to `/home/yourusername/helpdesk`

5. **Set up Database**
   - Go to "Databases" tab
   - Create a MySQL database
   - Update `.env` file with database credentials

6. **Configure WSGI file**
   - Edit the WSGI configuration file
   - Point it to `helpdesk.wsgi`

7. **Reload Web App**
   - Click "Reload" button
   - Your app will be live at `yourusername.pythonanywhere.com`

## Important Notes

### Email Configuration
To send emails, you need to:
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the app password as `EMAIL_HOST_PASSWORD`

### Database
- **Render**: Uses PostgreSQL by default (you may need to switch to MySQL or update settings)
- **Railway**: Provides MySQL addon
- **PythonAnywhere**: Provides MySQL database

### Static Files
- All platforms will run `python manage.py collectstatic` during deployment
- WhiteNoise is configured to serve static files efficiently

### Admin Access
After deployment, create a superuser:
```bash
python manage.py createsuperuser
```

Then access the admin panel at: `https://your-domain.com/admin/`

## Troubleshooting

1. **500 Error**: Check logs for detailed error messages
2. **Static files not loading**: Ensure `collectstatic` ran successfully
3. **Database connection issues**: Verify `DATABASE_URL` is set correctly
4. **Email not sending**: Check Gmail app password and SMTP settings

## Your Repository
GitHub: https://github.com/giftyarhin/helpdesk
