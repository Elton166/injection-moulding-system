# 🚀 Deployment Guide - Make Your App Live

## Overview
This guide covers multiple free deployment options to make your injection moulding app accessible online.

## 🌟 Recommended Free Platforms

### 1. **Render.com** (Easiest - Recommended)
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ PostgreSQL database included
- ✅ SSL certificate included
- ✅ Easy setup

### 2. **Railway.app**
- ✅ Free $5 credit monthly
- ✅ GitHub integration
- ✅ PostgreSQL included
- ✅ Very fast deployment

### 3. **PythonAnywhere**
- ✅ Free tier available
- ✅ Good for Django apps
- ✅ Manual deployment
- ✅ MySQL database

### 4. **Heroku** (Paid after Nov 2022)
- ⚠️ No longer free
- Still popular for production

---

## 🎯 Option 1: Deploy to Render.com (RECOMMENDED)

### Step 1: Prepare Your App

1. **Update requirements.txt**
Add these production dependencies:

```txt
gunicorn==21.2.0
psycopg2-binary==2.9.9
whitenoise==6.6.0
dj-database-url==2.1.0
```

2. **Create `build.sh` file** (for Render build commands):

```bash
#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python setup_troubleshooting.py
python setup_issues.py
```

3. **Update `settings.py`** (production settings):

Add at the top:
```python
import os
import dj_database_url
```

Update these settings:
```python
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com',  # Allow Render domains
]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Whitenoise for static files
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ... rest of middleware
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
```

### Step 2: Deploy to Render

1. **Go to Render.com**
   - Visit https://render.com
   - Sign up with your GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `Elton166/injection-moulding-system`
   - Click "Connect"

3. **Configure Service**
   - **Name**: `injection-moulding-system`
   - **Region**: Choose closest to you
   - **Branch**: `master`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn injection_moulding.wsgi:application`

4. **Add Environment Variables**
   Click "Advanced" and add:
   - `PYTHON_VERSION` = `3.11.0`
   - `DEBUG` = `False`
   - `SECRET_KEY` = (generate a new one - see below)
   - `DATABASE_URL` = (Render will auto-provide if you add PostgreSQL)

5. **Add PostgreSQL Database** (Optional but recommended)
   - Click "New +" → "PostgreSQL"
   - Name it and create
   - Copy the "Internal Database URL"
   - Add it as `DATABASE_URL` environment variable in your web service

6. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your app will be live at: `https://injection-moulding-system.onrender.com`

### Generate SECRET_KEY
Run this in Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 🎯 Option 2: Deploy to Railway.app

### Step 1: Prepare Your App (Same as Render)

Follow Step 1 from Render guide above.

### Step 2: Deploy to Railway

1. **Go to Railway.app**
   - Visit https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Elton166/injection-moulding-system`

3. **Add PostgreSQL**
   - Click "New" → "Database" → "Add PostgreSQL"
   - Railway auto-connects it

4. **Configure Settings**
   - Click on your service
   - Go to "Settings"
   - Add these variables:
     - `DEBUG` = `False`
     - `SECRET_KEY` = (your generated key)
     - `PORT` = `8000`

5. **Add Start Command**
   - In Settings → "Deploy"
   - Start Command: `gunicorn injection_moulding.wsgi:application --bind 0.0.0.0:$PORT`

6. **Deploy**
   - Railway auto-deploys
   - Get your URL from "Settings" → "Domains"
   - Click "Generate Domain"

---

## 🎯 Option 3: Deploy to PythonAnywhere

### Step 1: Sign Up
1. Go to https://www.pythonanywhere.com
2. Create free account (Beginner tier)

### Step 2: Upload Code
1. Open Bash console
2. Clone your repository:
```bash
git clone https://github.com/Elton166/injection-moulding-system.git
cd injection-moulding-system
```

### Step 3: Set Up Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Set paths:
   - Source code: `/home/yourusername/injection-moulding-system`
   - Working directory: `/home/yourusername/injection-moulding-system`
   - Virtualenv: `/home/yourusername/.virtualenvs/myenv`

### Step 5: Edit WSGI File
Click on WSGI configuration file and replace with:
```python
import os
import sys

path = '/home/yourusername/injection-moulding-system'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'injection_moulding.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 6: Set Up Static Files
In Web tab, add static files mapping:
- URL: `/static/`
- Directory: `/home/yourusername/injection-moulding-system/static`

### Step 7: Run Migrations
In Bash console:
```bash
cd injection-moulding-system
python manage.py migrate
python manage.py collectstatic
python setup_troubleshooting.py
python setup_issues.py
```

### Step 8: Reload
Click "Reload" button in Web tab

Your app will be live at: `https://yourusername.pythonanywhere.com`

---

## 📝 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] `DEBUG = False` in production
- [ ] `SECRET_KEY` is set via environment variable
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] Database is configured (PostgreSQL for production)
- [ ] Static files are configured with Whitenoise
- [ ] `requirements.txt` includes all dependencies
- [ ] Migrations are up to date
- [ ] Security settings are enabled
- [ ] Media files handling is configured (if needed)

---

## 🔒 Security Best Practices

1. **Never commit sensitive data**
   - Use environment variables
   - Add `.env` to `.gitignore`

2. **Use strong SECRET_KEY**
   - Generate new key for production
   - Never use the development key

3. **Enable HTTPS**
   - Most platforms provide free SSL
   - Set `SECURE_SSL_REDIRECT = True`

4. **Set secure cookies**
   - `SESSION_COOKIE_SECURE = True`
   - `CSRF_COOKIE_SECURE = True`

5. **Regular updates**
   - Keep Django and dependencies updated
   - Monitor security advisories

---

## 🎨 Custom Domain (Optional)

### For Render:
1. Go to Settings → Custom Domains
2. Add your domain
3. Update DNS records as instructed

### For Railway:
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS with provided CNAME

### For PythonAnywhere:
- Custom domains require paid plan

---

## 📊 Monitoring Your App

### Render:
- Built-in logs and metrics
- Email alerts for downtime

### Railway:
- Real-time logs
- Usage metrics dashboard

### PythonAnywhere:
- Error logs in Web tab
- Server logs available

---

## 🆘 Troubleshooting

### Common Issues:

**Static files not loading:**
```bash
python manage.py collectstatic --no-input
```

**Database errors:**
- Check DATABASE_URL is set correctly
- Run migrations: `python manage.py migrate`

**500 Internal Server Error:**
- Check logs for details
- Verify DEBUG=False
- Check ALLOWED_HOSTS

**Module not found:**
- Ensure all dependencies in requirements.txt
- Rebuild/redeploy

---

## 💰 Cost Comparison

| Platform | Free Tier | Database | SSL | Custom Domain |
|----------|-----------|----------|-----|---------------|
| Render | ✅ Yes | PostgreSQL | ✅ Free | ✅ Free |
| Railway | $5/month credit | PostgreSQL | ✅ Free | ✅ Free |
| PythonAnywhere | ✅ Yes | MySQL | ✅ Free | 💰 Paid |
| Heroku | ❌ No | PostgreSQL | ✅ Free | ✅ Free |

---

## 🚀 Quick Start (Render - Fastest)

1. Update requirements.txt with production packages
2. Create build.sh file
3. Update settings.py for production
4. Push to GitHub
5. Sign up on Render.com
6. Connect GitHub repo
7. Configure and deploy
8. Your app is live! 🎉

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- PythonAnywhere Help: https://help.pythonanywhere.com
- Django Deployment: https://docs.djangoproject.com/en/5.0/howto/deployment/

---

**Recommendation**: Start with **Render.com** - it's the easiest and most reliable free option for Django apps!
