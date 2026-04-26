# 🐍 PythonAnywhere Free Tier - Space Issue Fix

## Problem
The free tier only has 512MB storage, and OpenCV/image processing libraries are too large.

## Solution
Use the lightweight requirements file that excludes heavy packages.

---

## 🔧 Updated Installation Commands

In your PythonAnywhere Bash console:

```bash
# 1. Go to home directory
cd ~

# 2. Remove old installation if exists
rm -rf injection-moulding-system
rmvirtualenv myenv

# 3. Clone repository fresh
git clone https://github.com/Elton166/injection-moulding-system.git
cd injection-moulding-system

# 4. Create virtual environment
mkvirtualenv --python=/usr/bin/python3.10 myenv

# 5. Install LIGHTWEIGHT requirements (this is the key!)
pip install -r requirements-pythonanywhere.txt

# 6. Run migrations
python manage.py migrate

# 7. Collect static files
python manage.py collectstatic --no-input

# 8. Load initial data
python setup_troubleshooting.py
python setup_issues.py
```

---

## ✅ What's Different?

**Removed (too large for free tier):**
- ❌ opencv-python (300MB+)
- ❌ numpy (100MB+)
- ❌ scikit-image (50MB+)

**Kept (essential):**
- ✅ Django
- ✅ Pillow (for basic image handling)
- ✅ All other features

---

## 📊 Features That Still Work

✅ Company & Employee authentication
✅ Production orders
✅ Shift production tracking
✅ Material management
✅ Issue tracking
✅ Maintenance job cards
✅ Housekeeping tasks
✅ Mould runs
✅ Troubleshooting database
✅ Hourly checklists
✅ Master samples (upload only)

⚠️ **Disabled Feature:**
- Image comparison (requires OpenCV)
- You can still upload images, but automatic comparison won't work

---

## 🎯 Complete Fresh Start

Copy and paste these commands one by one:

```bash
# Clean everything
cd ~
rm -rf injection-moulding-system
rmvirtualenv myenv

# Fresh clone
git clone https://github.com/Elton166/injection-moulding-system.git
cd injection-moulding-system

# Create virtualenv
mkvirtualenv --python=/usr/bin/python3.10 myenv

# Install lightweight requirements
pip install -r requirements-pythonanywhere.txt

# Setup database
python manage.py migrate
python manage.py collectstatic --no-input
python setup_troubleshooting.py
python setup_issues.py

# Test it works
python manage.py check
```

---

## 📝 Web App Configuration

After installation, configure in Web tab:

**Source code:**
```
/home/yourusername/injection-moulding-system
```

**Working directory:**
```
/home/yourusername/injection-moulding-system
```

**Virtualenv:**
```
/home/yourusername/.virtualenvs/myenv
```

**WSGI file content:**
```python
import os
import sys

path = '/home/yourusername/injection-moulding-system'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'injection_moulding.settings'
os.environ['DEBUG'] = 'False'
os.environ['SECRET_KEY'] = 't24#vuj5f^d9dcw$c*39gqg9$g(m3v=uc6*nr1u7p&=6)x795_'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Static files:**
- URL: `/static/` → Directory: `/home/yourusername/injection-moulding-system/static`
- URL: `/media/` → Directory: `/home/yourusername/injection-moulding-system/media`

---

## ✅ Verification

After setup, verify everything works:

```bash
# Activate virtualenv
workon myenv

# Check Django is installed
python -c "import django; print('Django:', django.get_version())"

# Check app works
python manage.py check

# You should see: System check identified no issues
```

---

## 🎉 Success!

Your app should now work on PythonAnywhere free tier!

**What you get:**
- ✅ All core features working
- ✅ 100% free forever
- ✅ No credit card needed
- ✅ Professional URL

**Trade-off:**
- ⚠️ Image comparison disabled (requires paid tier for OpenCV)

---

## 💡 Alternative: Upgrade for Image Comparison

If you need image comparison:

**Option 1: PythonAnywhere Paid ($5/month)**
- More storage for OpenCV
- Use regular requirements.txt

**Option 2: Railway.app (Free $5 credit/month)**
- Enough resources for OpenCV
- All features work

**Option 3: Render.com**
- Free tier with more resources
- All features work

---

## 🆘 Still Having Space Issues?

Check your disk usage:
```bash
du -sh ~/*
```

Clean up if needed:
```bash
# Remove pip cache
rm -rf ~/.cache/pip

# Remove old virtualenvs
rmvirtualenv old_env_name
```

---

**Your app will be live at:**
`https://yourusername.pythonanywhere.com`

All features except image comparison will work perfectly! 🚀
