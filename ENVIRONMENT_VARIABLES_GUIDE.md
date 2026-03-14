# 🔐 Environment Variables Setup for Render

## What Are Environment Variables?

Environment variables are secure settings that your app needs to run in production. They keep sensitive information (like passwords and secret keys) out of your code.

---

## 📝 What to Add in Render

When you see "Environment Variables" in Render, click **"Add Environment Variable"** and add these **3 variables**:

### Variable 1: PYTHON_VERSION
```
Key: PYTHON_VERSION
Value: 3.11.0
```
**What it does**: Tells Render which Python version to use

---

### Variable 2: DEBUG
```
Key: DEBUG
Value: False
```
**What it does**: Turns off debug mode for security (never use True in production!)

---

### Variable 3: SECRET_KEY
```
Key: SECRET_KEY
Value: (generate this - see below)
```
**What it does**: Encrypts your sessions and passwords

#### How to Generate SECRET_KEY:

**Option A - Using Python (Recommended):**
1. Open your terminal/command prompt
2. Run this command:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
3. Copy the output (looks like: `django-insecure-a8f#k2$m...`)
4. Paste it as the SECRET_KEY value

**Option B - Using Online Generator:**
1. Go to https://djecrety.ir/
2. Click "Generate"
3. Copy the generated key
4. Paste it as the SECRET_KEY value

**Example SECRET_KEY:**
```
django-insecure-a8f#k2$m9p@x7w!z3v&n5q*r4t6y8u+i0o-p=s1d2f3g4h5j6k7l8m9n0
```

---

## 📋 Step-by-Step in Render

### 1. Find Environment Variables Section
After configuring your service, scroll down to find "Environment Variables" section.

### 2. Add First Variable
- Click **"Add Environment Variable"**
- In **Key** field, type: `PYTHON_VERSION`
- In **Value** field, type: `3.11.0`
- Click outside or press Enter

### 3. Add Second Variable
- Click **"Add Environment Variable"** again
- In **Key** field, type: `DEBUG`
- In **Value** field, type: `False`
- Click outside or press Enter

### 4. Add Third Variable
- Click **"Add Environment Variable"** again
- In **Key** field, type: `SECRET_KEY`
- In **Value** field, paste your generated secret key
- Click outside or press Enter

### 5. Done!
You should now see 3 environment variables listed:
```
PYTHON_VERSION = 3.11.0
DEBUG = False
SECRET_KEY = django-insecure-a8f#k2$m... (hidden)
```

---

## 🎯 Visual Example

```
┌─────────────────────────────────────────────┐
│ Environment Variables                        │
├─────────────────────────────────────────────┤
│                                             │
│ Key: PYTHON_VERSION                         │
│ Value: 3.11.0                               │
│                                             │
│ Key: DEBUG                                  │
│ Value: False                                │
│                                             │
│ Key: SECRET_KEY                             │
│ Value: django-insecure-a8f#k2$m9p@x7w!z... │
│                                             │
│ [+ Add Environment Variable]                │
│                                             │
└─────────────────────────────────────────────┘
```

---

## ❓ Common Questions

### Q: What if I skip this step?
**A:** Your app won't work! It needs these variables to run.

### Q: Can I change these later?
**A:** Yes! Go to your service → Settings → Environment Variables

### Q: Is my SECRET_KEY safe?
**A:** Yes! Render keeps it encrypted and hidden.

### Q: Do I need DATABASE_URL?
**A:** Not required initially. Add it later if you add PostgreSQL database.

---

## 🔒 Security Tips

1. **Never share your SECRET_KEY** - Keep it private!
2. **Never commit SECRET_KEY to GitHub** - Use environment variables only
3. **Always use DEBUG=False in production** - Never True!
4. **Generate a new SECRET_KEY for production** - Don't use the default one

---

## 🚀 After Adding Variables

Once you've added all 3 variables:

1. Scroll down
2. Select **Free** tier
3. Click **"Create Web Service"**
4. Render will start building your app
5. Wait 5-10 minutes
6. Your app will be live! 🎉

---

## 📊 Complete Checklist

Before clicking "Create Web Service", verify:

- [ ] PYTHON_VERSION = 3.11.0
- [ ] DEBUG = False
- [ ] SECRET_KEY = (your generated key, not the default one)
- [ ] Build Command = ./build.sh
- [ ] Start Command = gunicorn injection_moulding.wsgi:application
- [ ] Instance Type = Free

---

## 🆘 Troubleshooting

### Error: "SECRET_KEY not set"
**Fix:** Make sure you added SECRET_KEY environment variable

### Error: "Invalid SECRET_KEY"
**Fix:** Generate a new one using the Python command above

### App shows debug page
**Fix:** Make sure DEBUG = False (not True)

---

## 💡 Optional: Add Database Later

If you want to add PostgreSQL database:

1. Create PostgreSQL database in Render
2. Copy the "Internal Database URL"
3. Add new environment variable:
   - Key: `DATABASE_URL`
   - Value: (paste the database URL)
4. Your app will auto-redeploy with database

---

## ✅ Quick Reference

**Minimum Required Variables:**
```
PYTHON_VERSION = 3.11.0
DEBUG = False
SECRET_KEY = (your generated key)
```

**With Database (Optional):**
```
PYTHON_VERSION = 3.11.0
DEBUG = False
SECRET_KEY = (your generated key)
DATABASE_URL = (from PostgreSQL database)
```

---

## 🎊 You're Almost There!

After adding these 3 environment variables, you're ready to deploy! Just click "Create Web Service" and wait for your app to go live!

**Need the SECRET_KEY command again?**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Good luck! 🚀
