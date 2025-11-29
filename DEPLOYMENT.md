# Deployment Guide - Blockchain Voting System

This guide covers deploying your blockchain-based voting system to various cloud platforms.

---

## 📋 Table of Contents
1. [Railway.app](#1-railwayapp-recommended)
2. [Render.com](#2-rendercom)
3. [Heroku](#3-heroku)
4. [PythonAnywhere](#4-pythonanywhere)
5. [Vercel (with Python)](#5-vercel-with-python)
6. [Google Cloud Run](#6-google-cloud-run)
7. [AWS Elastic Beanstalk](#7-aws-elastic-beanstalk)
8. [DigitalOcean App Platform](#8-digitalocean-app-platform)
9. [Azure App Service](#9-azure-app-service)
10. [Fly.io](#10-flyio)
11. [Local Development](#local-development)

---

## 1. Railway.app ⭐ RECOMMENDED

**Cost:** $5/month free credit  
**Difficulty:** ⭐ Easy  
**Best For:** Quick deployments, demos, prototypes

### Prerequisites
- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))

### Deployment Steps

#### Option A: Deploy from GitHub (Easiest)

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/voting-system.git
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Flask and deploys!

3. **Get your URL:**
   - Click "Settings" → "Generate Domain"
   - Your app will be live at: `https://your-app.up.railway.app`

#### Option B: Deploy with Railway CLI

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   # or
   brew install railway
   ```

2. **Login and deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Open your app:**
   ```bash
   railway open
   ```

### Configuration Files (Already Created)
- ✅ `railway.json` - Railway configuration
- ✅ `Procfile` - Process file
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python version

### Environment Variables (Optional)
In Railway dashboard, add:
- `DEBUG=False` (for production)
- `SECRET_KEY=your-secret-key-here`

---

## 2. Render.com

**Cost:** Free tier available  
**Difficulty:** ⭐ Easy  
**Best For:** Free hosting, automatic deployments

### Deployment Steps

1. **Push code to GitHub** (same as Railway)

2. **Create Render account:** [render.com](https://render.com)

3. **Create new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** blockchain-voting-system
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
     - **Plan:** Free

4. **Deploy:** Click "Create Web Service"

5. **Your app will be live at:** `https://your-app.onrender.com`

### Additional Configuration

Create `render.yaml` for advanced config:
```yaml
services:
  - type: web
    name: blockchain-voting
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.13.0
      - key: DEBUG
        value: false
```

---

## 3. Heroku

**Cost:** $5/month minimum (no free tier as of 2022)  
**Difficulty:** ⭐⭐ Medium  
**Best For:** Production apps, established platform

### Deployment Steps

1. **Install Heroku CLI:**
   ```bash
   brew tap heroku/brew && brew install heroku
   # or download from heroku.com/cli
   ```

2. **Login:**
   ```bash
   heroku login
   ```

3. **Create app:**
   ```bash
   heroku create your-voting-app
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Open app:**
   ```bash
   heroku open
   ```

### Configuration Files (Already Created)
- ✅ `Procfile`
- ✅ `requirements.txt`
- ✅ `runtime.txt`

### Set Environment Variables:
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
```

---

## 4. PythonAnywhere

**Cost:** Free tier available  
**Difficulty:** ⭐⭐⭐ Medium  
**Best For:** Python-specific hosting

### Deployment Steps

1. **Sign up:** [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload code:**
   - Go to "Files" tab
   - Upload your project files or clone from GitHub

3. **Create virtual environment:**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 votingenv
   pip install -r requirements.txt
   ```

4. **Configure Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Select Python 3.10

5. **Configure WSGI file:**
   Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
   ```python
   import sys
   path = '/home/yourusername/VotingSystem'
   if path not in sys.path:
       sys.path.append(path)

   from app import app as application
   ```

6. **Reload web app**

---

## 5. Vercel (with Python)

**Cost:** Free tier available  
**Difficulty:** ⭐⭐ Medium  
**Best For:** Serverless deployments

### Setup

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Create `vercel.json`:**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

**Note:** Vercel has execution time limits on free tier.

---

## 6. Google Cloud Run

**Cost:** Free tier with limits  
**Difficulty:** ⭐⭐⭐⭐ Advanced  
**Best For:** Scalable containerized apps

### Prerequisites
- Google Cloud account
- Docker installed

### Deployment Steps

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.13-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
   ```

2. **Build and deploy:**
   ```bash
   gcloud init
   gcloud builds submit --tag gcr.io/PROJECT-ID/voting-system
   gcloud run deploy --image gcr.io/PROJECT-ID/voting-system --platform managed
   ```

---

## 7. AWS Elastic Beanstalk

**Cost:** Pay-as-you-go  
**Difficulty:** ⭐⭐⭐⭐ Advanced  
**Best For:** AWS ecosystem, scalability

### Setup

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize:**
   ```bash
   eb init -p python-3.13 voting-system
   ```

3. **Create environment and deploy:**
   ```bash
   eb create voting-env
   eb deploy
   ```

4. **Open app:**
   ```bash
   eb open
   ```

---

## 8. DigitalOcean App Platform

**Cost:** $5/month minimum  
**Difficulty:** ⭐⭐ Medium  
**Best For:** Simple deployment with DO infrastructure

### Deployment Steps

1. **Push to GitHub**

2. **Go to:** [cloud.digitalocean.com/apps](https://cloud.digitalocean.com/apps)

3. **Create App:**
   - Select GitHub repository
   - Choose region
   - Configure:
     - **Type:** Web Service
     - **Run Command:** `gunicorn app:app`

4. **Deploy:** Click "Launch App"

---

## 9. Azure App Service

**Cost:** Free tier available  
**Difficulty:** ⭐⭐⭐ Medium-Advanced  
**Best For:** Microsoft ecosystem

### Deployment Steps

1. **Install Azure CLI:**
   ```bash
   brew install azure-cli
   ```

2. **Login:**
   ```bash
   az login
   ```

3. **Create app:**
   ```bash
   az webapp up --name voting-system --runtime "PYTHON:3.13"
   ```

---

## 10. Fly.io

**Cost:** Free tier available  
**Difficulty:** ⭐⭐ Medium  
**Best For:** Global edge deployment

### Deployment Steps

1. **Install Fly CLI:**
   ```bash
   brew install flyctl
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Launch app:**
   ```bash
   fly launch
   ```

4. **Deploy:**
   ```bash
   fly deploy
   ```

---

## Local Development

### Running Locally

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```

4. **Access at:** http://127.0.0.1:5000

### With Gunicorn (Production-like)

```bash
gunicorn app:app --bind 127.0.0.1:5000 --reload
```

---

## 🎯 Quick Comparison

| Platform | Free Tier | Ease | Best For |
|----------|-----------|------|----------|
| **Railway.app** | $5 credit | ⭐ | Quick demos |
| **Render.com** | Yes | ⭐ | Free hosting |
| **Heroku** | No ($5/mo) | ⭐⭐ | Production |
| **PythonAnywhere** | Yes (limited) | ⭐⭐⭐ | Python apps |
| **Vercel** | Yes | ⭐⭐ | Serverless |
| **Google Cloud Run** | Yes (limits) | ⭐⭐⭐⭐ | Containers |
| **AWS EB** | Free trial | ⭐⭐⭐⭐ | AWS users |
| **DigitalOcean** | No ($5/mo) | ⭐⭐ | Simple apps |
| **Azure** | Yes (limited) | ⭐⭐⭐ | Azure users |
| **Fly.io** | Yes | ⭐⭐ | Edge hosting |

---

## 🔧 Environment Variables

For production deployments, set these environment variables:

```bash
# Required
PORT=5000                    # Auto-set by most platforms
DEBUG=False                  # Disable debug mode in production
SECRET_KEY=your-secret-key   # Generate with: python -c "import secrets; print(secrets.token_hex(32))"

# Optional
HOST=0.0.0.0                # Allow external connections
```

---

## 🚨 Important Notes

### Data Persistence Warning
Your app currently stores data in memory. On server restart:
- ❌ All elections are lost
- ❌ All voters are lost
- ❌ All votes are lost

**For production, you need:**
1. Database (PostgreSQL, MongoDB, SQLite)
2. Session management
3. File storage or cloud storage

### Security Considerations
Before deploying to production:
1. Change `DEBUG=False`
2. Generate a secure `SECRET_KEY`
3. Add rate limiting
4. Add HTTPS (most platforms provide this)
5. Add authentication for admin portal
6. Validate all inputs
7. Add CORS if needed

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Render Documentation](https://render.com/docs)
- [Heroku Python Guide](https://devcenter.heroku.com/articles/getting-started-with-python)
- [Flask Deployment Options](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

## 🆘 Troubleshooting

### Common Issues

**Issue:** "Module not found" error
```bash
# Solution: Make sure requirements.txt is correct
pip freeze > requirements.txt
```

**Issue:** Port binding error
```bash
# Solution: Use PORT from environment
port = int(os.environ.get('PORT', 5000))
```

**Issue:** Static files not loading
```bash
# Solution: Check Flask static folder configuration
app = Flask(__name__, static_folder='static')
```

---

## ✅ Pre-Deployment Checklist

- [ ] All files committed to Git
- [ ] `.gitignore` configured
- [ ] `requirements.txt` up to date
- [ ] `Procfile` created
- [ ] `runtime.txt` specifies Python version
- [ ] `DEBUG=False` in production
- [ ] Secret key configured
- [ ] Tested locally with Gunicorn
- [ ] Static files working
- [ ] All routes tested

---

**Ready to deploy?** I recommend starting with **Railway.app** or **Render.com** for the easiest experience!
