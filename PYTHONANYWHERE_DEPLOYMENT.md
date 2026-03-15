# 🐍 Deploy to PythonAnywhere - 100% FREE FOREVER

## Why PythonAnywhere?
- ✅ Completely FREE (no credit card needed)
- ✅ Never expires
- ✅ Made for Python/Django
- ✅ MySQL database included
- ✅ Easy to use

---

## 📋 Step-by-Step Deployment Guide

### Step 1: Create Account (2 minutes)

1. Go to https://www.pythonanywhere.com
2. Click **"Start running Python online in less than a minute!"**
3. Click **"Create a Beginner account"** (FREE)
4. Fill in:
   - Username (this will be in your URL)
   - Email
   - Password
5. Click **"Register"**
6. Verify your email

---

### Step 2: Open Bash Console (1 minute)

1. After login, you'll see the Dashboard
2. Click **"Consoles"** tab at the top
3. Under "Start a new console", click **"Bash"**
4. A terminal window opens

---

### Step 3: Clone Your Repository (2 minutes)

In the Bash console, type these commands:

```bash
git clone https://github.com/Elton166/injection-moulding-system.git
cd injection-moulding-system
```

Press Enter after each command.

---

### Step 4: Create Virtual Environment (3 minutes)

```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
```

You'll see `(myenv)` appear before your prompt.

---

### Step 5: Install Dependencies (5 minutes)

```bash
pip install -r requirements.txt
```

Wait for all packages to install (this takes a few minutes).

---

### Step 6: Create Web App (3 minutes)

1. Click **"Web"** tab at the top
2. Click **"Add a new web app"**
3. Click **"Next"** (for your domain)
4. Select **"Manual configuration"**
5. Select **"Python 3.10"**
6. Click **"Next"**

---

### Step 7: Configure Paths (5 minutes)

On the Web tab, you'll see configuration sections:

#### A. Source Code
Find "Code" section:
- **Source code**: `/home/yourusername/injection-moulding-system`
- **Working directory**: `/home/yourusername/injection-moulding-system`

(Replace `yourusername` with your actual PythonAnywhere username)

#### B. Virtualenv
Find "Virtualenv" section:
- Click the link "Enter path to a virtualenv"
- Enter: `/home/yourusername/.virtualenvs/myenv`
- Click ✓ (checkmark)

---

### Step 8: Configure WSGI File (5 minutes)

1. In the "Code" section, find **"WSGI configuration file"**
2. Click the link (looks like `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **Delete everything** in the file
4. **Copy and paste this** (replace `yourusername` with yours):

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/injection-moulding-system'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'injection_moulding.settings'
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 't24#vuj5f^d9dcw$c*39gqg9$g(m3v=uc6*nr1u7p&=6)x795_'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. Click **"Save"** (top right)

---

### Step 9: Configure Static Files (3 minutes)

On the Web tab, scroll to "Static files" section:

Click **"Enter URL"** and add:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/injection-moulding-system/static` |
| `/media/` | `/home/yourusername/injection-moulding-system/media` |

(Replace `yourusername` with your actual username)

---

### Step 10: Run Migrations (3 minutes)

Go back to your **Bash console** (or open a new one):

```bash
cd injection-moulding-system
workon myenv
python manage.py migrate
python manage.py collectstatic --no-input
python setup_troubleshooting.py
python setup_issues.py
```

---

### Step 11: Update Settings for PythonAnywhere (2 minutes)

In Bash console:

```bash
nano injection_moulding/settings.py
```

Find `ALLOWED_HOSTS` and make sure it includes:
```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.pythonanywhere.com',
    'yourusername.pythonanywhere.com',
]
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

---

### Step 12: Reload Web App (1 minute)

1. Go back to **"Web"** tab
2. Scroll to top
3. Click the big green **"Reload yourusername.pythonanywhere.com"** button
4. Wait 10 seconds

---

### Step 13: Visit Your Live App! 🎉

Your app is now live at:
```
https://yourusername.pythonanywhere.com
```

(Replace `yourusername` with your actual username)

---

## ✅ Success Checklist

- [ ] Account created
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Web app created
- [ ] Paths configured
- [ ] WSGI file updated
- [ ] Static files configured
- [ ] Migrations run
- [ ] Settings updated
- [ ] Web app reloaded
- [ ] App is live!

---

## 🔧 Troubleshooting

### Error: "ImportError: No module named django"
**Fix**: Make sure virtualenv is configured correctly in Web tab

### Error: "DisallowedHost"
**Fix**: Add your domain to ALLOWED_HOSTS in settings.py

### Static files not loading
**Fix**: 
```bash
python manage.py collectstatic --no-input
```
Then reload web app

### Database errors
**Fix**: Make sure migrations ran:
```bash
python manage.py migrate
```

### View Error Logs
1. Go to Web tab
2. Scroll to "Log files"
3. Click "Error log" to see errors
4. Click "Server log" to see requests

---

## 🔄 Making Updates

When you update your code on GitHub:

```bash
cd injection-moulding-system
git pull origin master
workon myenv
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input
```

Then reload web app in Web tab.

---

## 💾 Create Superuser (Optional)

To access Django admin:

```bash
cd injection-moulding-system
workon myenv
python manage.py createsuperuser
```

Follow prompts to create admin account.

Access admin at: `https://yourusername.pythonanywhere.com/admin/`

---

## 📊 Free Tier Limitations

- CPU: Limited (enough for small apps)
- Storage: 512 MB
- One web app
- MySQL database (not PostgreSQL)
- App sleeps after inactivity (wakes on request)

**Good news**: These limits are fine for your app!

---

## 🎯 Quick Commands Reference

**Activate virtualenv:**
```bash
workon myenv
```

**Update code:**
```bash
cd injection-moulding-system
git pull
```

**Run migrations:**
```bash
python manage.py migrate
```

**Collect static files:**
```bash
python manage.py collectstatic --no-input
```

**View logs:**
Go to Web tab → Log files section

---

## 🆘 Need Help?

- PythonAnywhere Help: https://help.pythonanywhere.com
- Forums: https://www.pythonanywhere.com/forums/
- Django on PythonAnywhere: https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/

---

## 🎉 Congratulations!

Your app is now live and FREE FOREVER at:
**https://yourusername.pythonanywhere.com**

Share it with:
- Friends and family
- Potential employers
- LinkedIn
- Your portfolio

---

**Total Time**: ~30 minutes
**Cost**: $0 (FREE FOREVER!)
**Your Live URL**: `https://yourusername.pythonanywhere.com`

Enjoy your live app! 🚀
