# 🚀 Quick Deploy to Render.com

## Prerequisites
- GitHub account with your code pushed
- Render.com account (free)

## Step-by-Step Deployment

### 1. Sign Up on Render
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your GitHub account

### 2. Create New Web Service
1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect account" to link GitHub
4. Find and select your repository: `injection-moulding-system`
5. Click "Connect"

### 3. Configure Your Service

Fill in these settings:

**Basic Settings:**
- **Name**: `injection-moulding-system` (or your preferred name)
- **Region**: Choose closest to your location
- **Branch**: `master`
- **Root Directory**: (leave blank)
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn injection_moulding.wsgi:application`

**Instance Type:**
- Select **Free** tier

### 4. Add Environment Variables

Click "Advanced" button, then add these environment variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate using command below |

**To generate SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste as SECRET_KEY value.

### 5. Add PostgreSQL Database (Recommended)

1. Click "New +" → "PostgreSQL"
2. **Name**: `injection-moulding-db`
3. **Database**: `injection_moulding`
4. **User**: `injection_moulding_user`
5. Click "Create Database"
6. Wait for database to be created
7. Go back to your Web Service
8. In Environment Variables, add:
   - **Key**: `DATABASE_URL`
   - **Value**: Copy "Internal Database URL" from your PostgreSQL database

### 6. Deploy!

1. Click "Create Web Service" button
2. Wait 5-10 minutes for deployment
3. Watch the logs for any errors
4. Once deployed, you'll see "Live" status

### 7. Access Your App

Your app will be available at:
```
https://injection-moulding-system.onrender.com
```
(Replace with your actual service name)

### 8. Create Superuser (Optional)

1. Go to your service dashboard
2. Click "Shell" tab
3. Run:
```bash
python manage.py createsuperuser
```
4. Follow prompts to create admin account

## 🎉 Your App is Live!

You can now:
- Access your app at the Render URL
- Register companies and users
- Use all features online
- Share the URL with others

## 📝 Important Notes

### Free Tier Limitations:
- App sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- 750 hours/month free (enough for one app)
- Database: 90 days retention, then deleted if inactive

### Keeping App Awake:
Use a service like:
- UptimeRobot (https://uptimerobot.com)
- Cron-job.org (https://cron-job.org)

Set it to ping your app every 10 minutes.

### Custom Domain (Optional):
1. Go to Settings → Custom Domains
2. Add your domain
3. Update DNS records as instructed
4. Free SSL certificate included!

## 🔄 Automatic Deployments

Render automatically deploys when you push to GitHub:

1. Make changes locally
2. Commit and push to GitHub:
```bash
git add .
git commit -m "Your changes"
git push origin master
```
3. Render automatically detects and deploys
4. Wait 2-5 minutes for deployment

## 🐛 Troubleshooting

### Build Failed:
- Check build logs for errors
- Ensure `build.sh` has execute permissions
- Verify all dependencies in requirements.txt

### App Not Loading:
- Check if DEBUG=False
- Verify ALLOWED_HOSTS includes `.onrender.com`
- Check application logs

### Static Files Not Loading:
- Ensure Whitenoise is in MIDDLEWARE
- Run `python manage.py collectstatic` in shell
- Check STATIC_ROOT is set correctly

### Database Errors:
- Verify DATABASE_URL is set
- Check database is running
- Run migrations in shell: `python manage.py migrate`

### View Logs:
1. Go to your service dashboard
2. Click "Logs" tab
3. View real-time logs

### Access Shell:
1. Go to your service dashboard
2. Click "Shell" tab
3. Run Django commands

## 💡 Pro Tips

1. **Monitor Your App**: Check logs regularly
2. **Set Up Alerts**: Enable email notifications in Settings
3. **Use PostgreSQL**: More reliable than SQLite for production
4. **Keep Dependencies Updated**: Regularly update requirements.txt
5. **Backup Database**: Export data regularly

## 📊 After Deployment

### Test Everything:
- [ ] Company registration works
- [ ] Employee login works
- [ ] Create production orders
- [ ] Upload images
- [ ] Check all features
- [ ] Test on mobile devices

### Share Your App:
- Add to your portfolio
- Share on LinkedIn
- Add to your resume
- Show to potential employers

## 🆘 Need Help?

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/

---

**Congratulations! Your app is now live and accessible worldwide! 🎉**
