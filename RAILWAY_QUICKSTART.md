# Quick Deployment to Railway.app

This guide will help you deploy your Blockchain Voting System to Railway.app in under 5 minutes.

## Prerequisites
- GitHub account
- Git installed
- Railway account (free - sign up at https://railway.app)

## Step-by-Step Deployment

### 1. Prepare Your Repository

```bash
# Navigate to your project directory
cd /Users/I527873/Documents/BITS/VotingSystem

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit - Ready for deployment"
```

### 2. Push to GitHub

```bash
# Create a new repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 3. Deploy on Railway

#### Option A: Web Interface (Easiest)

1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Click **"Deploy from GitHub repo"**
4. Select your repository
5. Railway will automatically:
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Use the `Procfile` to start your app
   - Assign a public URL

6. Click **"Settings"** → **"Generate Domain"**
7. Your app is live! 🎉

#### Option B: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli
# or
brew install railway

# Login
railway login

# Initialize project
railway init

# Deploy
railway up

# Open your app
railway open
```

### 4. Access Your App

Your app will be available at:
```
https://your-app-name.up.railway.app
```

Access points:
- **Home:** https://your-app-name.up.railway.app/
- **Admin:** https://your-app-name.up.railway.app/admin
- **Voter:** https://your-app-name.up.railway.app/voter
- **Results:** https://your-app-name.up.railway.app/results

## Configuration (Optional)

### Environment Variables

In Railway dashboard, go to **Variables** and add:

```bash
DEBUG=False              # Disable debug mode for production
SECRET_KEY=your-key      # Generate with: python -c "import secrets; print(secrets.token_hex(32))"
```

### Custom Domain

1. Go to **Settings** → **Domains**
2. Click **"Custom Domain"**
3. Add your domain (requires DNS configuration)

## Files Already Configured

✅ **Procfile** - Tells Railway how to run your app
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

✅ **railway.json** - Railway-specific configuration
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app --bind 0.0.0.0:$PORT"
  }
}
```

✅ **requirements.txt** - Python dependencies
```
Flask==3.0.0
gunicorn==21.2.0
requests==2.31.0
```

✅ **runtime.txt** - Python version
```
python-3.13.0
```

✅ **.gitignore** - Files to exclude from git

## Local Testing

Test your deployment configuration locally:

```bash
# With Python's built-in server (development)
python app.py

# With Gunicorn (production-like)
gunicorn app:app --bind 127.0.0.1:5000 --reload
```

## Monitoring

Railway provides:
- **Logs:** Real-time application logs
- **Metrics:** CPU, Memory, Network usage
- **Deployments:** History of all deployments

Access these in your Railway project dashboard.

## Troubleshooting

### Port Issues
Railway automatically sets the `PORT` environment variable. Your app is already configured to use it:
```python
port = int(os.environ.get('PORT', 5000))
```

### Dependencies Not Installing
Make sure `requirements.txt` is in the root directory and contains all dependencies:
```bash
pip freeze > requirements.txt
```

### Application Not Starting
Check Railway logs for errors:
1. Go to your project
2. Click on the deployment
3. View logs tab

### Static Files Not Loading
Railway serves static files automatically. Make sure your `static` folder structure is correct:
```
VotingSystem/
├── static/
│   ├── css/
│   └── js/
└── templates/
```

## Cost

Railway offers:
- **Free:** $5 credit per month (sufficient for demos/testing)
- **Hobby:** $5/month for more resources
- **Pro:** $20/month for production apps

Your app should run comfortably on the free tier for demos and testing.

## Data Persistence Warning

⚠️ **Important:** Your app currently stores data in memory. When Railway restarts your container:
- All elections are lost
- All voters are lost
- All votes are lost

For production use, consider adding database persistence (PostgreSQL, MongoDB, etc.)

## Next Steps

After deployment:
1. Test all features on the live URL
2. Create sample elections
3. Share the URL with users
4. Monitor logs and performance
5. Consider adding database persistence for production use

## Support

- **Railway Docs:** https://docs.railway.app
- **Community:** https://discord.gg/railway
- **Status:** https://status.railway.app

---

**Your app is ready to deploy!** Just push to GitHub and connect to Railway. 🚀
