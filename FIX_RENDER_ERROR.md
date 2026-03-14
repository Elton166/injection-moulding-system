# 🔧 Fix: ModuleNotFoundError: No module named 'app'

## The Problem
Render is looking for a module called `app` but your Django project is called `injection_moulding`.

## The Solution

### Step 1: Go to Your Render Service
1. Open your Render dashboard
2. Click on your service: `injection-moulding-system`
3. Click on **"Settings"** (left sidebar)

### Step 2: Update Start Command
Scroll down to find **"Start Command"**

**Change it from:**
```bash
gunicorn app.wsgi:application
```

**To:**
```bash
gunicorn injection_moulding.wsgi:application
```

### Step 3: Verify Build Command
Make sure **"Build Command"** is set to:
```bash
./build.sh
```

**OR if that doesn't work, use:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

### Step 4: Save and Redeploy
1. Click **"Save Changes"** at the bottom
2. Render will automatically redeploy
3. Wait 5-10 minutes
4. Check the logs - it should work now! ✅

---

## Complete Configuration Checklist

Before deploying, verify these settings in Render:

### Basic Settings:
- ✅ **Name**: `injection-moulding-system`
- ✅ **Branch**: `master`
- ✅ **Runtime**: `Python 3`

### Build & Deploy:
- ✅ **Build Command**: `./build.sh` OR `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
- ✅ **Start Command**: `gunicorn injection_moulding.wsgi:application`

### Environment Variables:
- ✅ `PYTHON_VERSION` = `3.11.0`
- ✅ `DEBUG` = `False`
- ✅ `SECRET_KEY` = `t24#vuj5f^d9dcw$c*39gqg9$g(m3v=uc6*nr1u7p&=6)x795_`

---

## Alternative: Manual Redeploy

If auto-deploy doesn't trigger:

1. Go to your service dashboard
2. Click **"Manual Deploy"** button (top right)
3. Select **"Deploy latest commit"**
4. Click **"Deploy"**

---

## Watch the Logs

After saving changes:

1. Click **"Logs"** tab
2. Watch for these success messages:
   ```
   Installing collected packages...
   Successfully installed...
   Collecting static files...
   Running migrations...
   Starting gunicorn...
   Listening at: http://0.0.0.0:10000
   ```

3. When you see "Listening at", your app is LIVE! 🎉

---

## If You Still Get Errors

### Error: "Permission denied: ./build.sh"
**Fix**: Change Build Command to:
```bash
bash build.sh
```

### Error: "collectstatic failed"
**Fix**: Add to Environment Variables:
```
DISABLE_COLLECTSTATIC = 1
```

### Error: Database connection
**Fix**: Add PostgreSQL database and set DATABASE_URL

---

## Success Indicators

You'll know it worked when you see:

✅ Build status: **Live** (green)
✅ Logs show: "Listening at: http://0.0.0.0:10000"
✅ Your URL works: `https://injection-moulding-system.onrender.com`

---

## Quick Summary

**The main fix:**
Change Start Command to: `gunicorn injection_moulding.wsgi:application`

That's it! This should fix the "No module named 'app'" error.
