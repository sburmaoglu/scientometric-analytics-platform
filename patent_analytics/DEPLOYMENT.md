# Deployment Guide

## Option 1: Streamlit Community Cloud (Recommended for MVP) - 100% FREE

### Prerequisites
- GitHub account
- Streamlit Community Cloud account (free)

### Steps

1. **Push to GitHub**
```bash
cd patent_analytics
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/patent-analytics.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `app.py`
   - Click "Deploy"

3. **Done!**
   - Your app will be live at: `https://yourusername-patent-analytics.streamlit.app`
   - Free hosting with automatic updates on git push
   - SSL certificate included
   - Custom domain support (optional)

### Limits (Free Tier)
- 1 GB RAM
- 1 CPU
- Community support only
- Apps sleep after inactivity (wake up on first request)

---

## Option 2: Render (Free Tier)

### Steps

1. **Create `render.yaml`** (already included in repo)

2. **Push to GitHub**

3. **Deploy on Render**
   - Go to https://render.com
   - Sign up (free)
   - Click "New" → "Web Service"
   - Connect GitHub repo
   - Select branch: main
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - Click "Create Web Service"

### Limits (Free Tier)
- 512 MB RAM
- Shared CPU
- Apps spin down after 15 minutes of inactivity
- Free SSL certificate
- Custom domain support

---

## Option 3: Railway (Free Trial)

### Steps

1. **Install Railway CLI** (optional)
```bash
npm install -g @railway/cli
```

2. **Deploy**
   - Go to https://railway.app
   - Sign up (free)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repo
   - Railway auto-detects Python and installs dependencies
   - Set start command: `streamlit run app.py`

### Limits (Free Trial)
- $5 free credit (usually lasts 1-2 months for MVP)
- Then ~$5/month for small apps
- Better performance than free tiers

---

## Option 4: Heroku (Paid)

### Steps

1. **Create `Procfile`**
```
web: sh setup.sh && streamlit run app.py
```

2. **Create `setup.sh`**
```bash
mkdir -p ~/.streamlit/
echo "[server]
port = $PORT
headless = true
enableCORS = false
" > ~/.streamlit/config.toml
```

3. **Deploy**
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### Cost
- ~$7/month for basic dyno
- Better performance and reliability
- Easy scaling

---

## Option 5: DigitalOcean App Platform

### Steps

1. **Push to GitHub**

2. **Create App on DigitalOcean**
   - Go to https://cloud.digitalocean.com/apps
   - Click "Create App"
   - Connect GitHub
   - Select repository
   - Detect Python app
   - Set run command: `streamlit run app.py`

### Cost
- $5/month for basic tier
- Good performance
- Easy scaling

---

## Option 6: AWS / GCP / Azure (Production)

### Recommended Setup

**Architecture:**
```
Users → Load Balancer → App Servers (Streamlit) → Database → Storage
```

**AWS Example:**
- EC2 instances with Auto Scaling
- RDS for PostgreSQL
- S3 for file storage
- CloudFront for CDN
- Route 53 for DNS

**Cost:** ~$50-200/month depending on usage

---

## Local Development

### Setup

1. **Create virtual environment**
```bash
cd patent_analytics
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run locally**
```bash
streamlit run app.py
```

4. **Open browser**
```
http://localhost:8501
```

---

## Environment Variables (for AI features in Phase 2)

Create `.streamlit/secrets.toml`:

```toml
# API Keys
ANTHROPIC_API_KEY = "your-key-here"
OPENAI_API_KEY = "your-key-here"

# Database (if using)
DATABASE_URL = "postgresql://..."

# Stripe (for payments)
STRIPE_PUBLIC_KEY = "pk_..."
STRIPE_SECRET_KEY = "sk_..."
```

**Never commit secrets to git!**

---

## Performance Optimization

### For Production

1. **Add caching**
```python
@st.cache_data
def load_data(file):
    return pd.read_csv(file)
```

2. **Use session state wisely**
```python
if 'data' not in st.session_state:
    st.session_state.data = None
```

3. **Optimize imports**
```python
# Load heavy libraries only when needed
if need_analysis:
    import networkx as nx
```

4. **Add loading indicators**
```python
with st.spinner('Processing...'):
    result = heavy_computation()
```

---

## Monitoring & Analytics

### Streamlit Cloud
- Built-in metrics dashboard
- App logs
- Error tracking

### Production
- Google Analytics
- Sentry for error tracking
- Prometheus + Grafana for metrics
- Cloudwatch/Stackdriver for AWS/GCP

---

## Recommended Approach for Your Project

### Phase 1 (Now - MVP Testing)
**Use: Streamlit Community Cloud (FREE)**
- Get user feedback
- Test the concept
- No cost
- Easy to iterate

### Phase 2 (With Users)
**Use: Railway or Render ($5-10/month)**
- Better performance
- No sleep time
- Support for background tasks
- Add database if needed

### Phase 3 (Growing)
**Use: DigitalOcean or AWS ($50-200/month)**
- Scale based on usage
- Professional infrastructure
- Custom domain
- Better support

---

## Next Steps

1. ✅ Complete the MVP features (we'll do this together)
2. 🚀 Deploy to Streamlit Cloud (free)
3. 👥 Get 10-20 beta users
4. 📊 Collect feedback
5. 🔄 Iterate based on feedback
6. 💰 Add payment integration (Stripe)
7. 🎯 Launch publicly

## Need Help?

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Forum: https://discuss.streamlit.io
- This guide: Keep it handy!
