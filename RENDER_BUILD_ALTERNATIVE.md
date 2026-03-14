# Alternative Render Build Configuration

If `./build.sh` is causing issues, use this alternative configuration:

## Option 1: Direct Build Command

Instead of `./build.sh`, use this as your Build Command in Render:

```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python setup_troubleshooting.py && python setup_issues.py
```

## Option 2: Use bash explicitly

```bash
bash build.sh
```

## Option 3: Use sh

```bash
sh build.sh
```

## Complete Render Configuration

**Build Command (choose one):**
- Option 1: `pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate`
- Option 2: `bash build.sh`
- Option 3: `sh build.sh`

**Start Command:**
```bash
gunicorn injection_moulding.wsgi:application
```

**Environment Variables:**
```
PYTHON_VERSION = 3.11.0
DEBUG = False
SECRET_KEY = t24#vuj5f^d9dcw$c*39gqg9$g(m3v=uc6*nr1u7p&=6)x795_
```

## If Build Still Fails

1. Check the exact error in Render logs
2. Common issues:
   - Missing dependencies in requirements.txt
   - Python version mismatch
   - Database connection issues
   - Static files configuration

## Minimal Build (Skip Initial Data)

If setup scripts are causing issues, use minimal build:

```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

You can run setup scripts later from the Render shell.
