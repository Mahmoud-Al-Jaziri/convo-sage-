# Deployment Guide

Complete guide for deploying ConvoSage to production.

---

## 🎯 Deployment Options

### Recommended Stack
- **Backend**: Render / Railway / Fly.io
- **Frontend**: Vercel / Netlify
- **Database**: Railway PostgreSQL (or keep SQLite)

---

## 🚀 Option 1: Quick Deploy (Recommended)

### Backend → Render

#### 1. Prepare Backend

```bash
cd backend

# Create render.yaml (Render configuration)
cat > render.yaml << 'EOF'
services:
  - type: web
    name: convosage-api
    env: python
    buildCommand: "pip install -r requirements.txt && python scripts/ingest_outlets.py"
    startCommand: "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: ENVIRONMENT
        value: production
EOF
```

#### 2. Deploy to Render

1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Connect your `convo-sage` repository
5. Select `backend/` as root directory
6. Render will auto-detect `render.yaml`
7. Click "Create Web Service"

**Your API will be at:** `https://convosage-api.onrender.com`

---

### Frontend → Vercel

#### 1. Prepare Frontend

```bash
cd frontend

# Create .env.production
echo "VITE_API_URL=https://convosage-api.onrender.com" > .env.production

# Update vite.config.js for production
cat > vite.config.js << 'EOF'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: false
  }
})
EOF
```

#### 2. Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

Or via Vercel Dashboard:
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Select `frontend/` as root directory
4. Add environment variable: `VITE_API_URL=https://convosage-api.onrender.com`
5. Click "Deploy"

**Your app will be at:** `https://convosage.vercel.app`

---

## 🚀 Option 2: Railway (Full Stack)

### Deploy Both Backend & Frontend

#### 1. Install Railway CLI

```bash
npm install -g @railway/cli
railway login
```

#### 2. Deploy Backend

```bash
cd backend

# Initialize Railway
railway init

# Add PostgreSQL (optional, or keep SQLite)
railway add -d postgresql

# Set environment variables
railway variables set ENVIRONMENT=production
railway variables set PYTHON_VERSION=3.10.0

# Deploy
railway up
```

#### 3. Deploy Frontend

```bash
cd frontend

# Build
npm run build

# Deploy static files to Railway or Vercel
railway up --service frontend
```

---

## 🐳 Option 3: Docker Deployment

### Create Docker Files

#### Backend Dockerfile

```bash
cd backend
cat > Dockerfile << 'EOF'
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Ingest data
RUN python scripts/ingest_outlets.py

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF
```

#### Frontend Dockerfile

```bash
cd frontend
cat > Dockerfile << 'EOF'
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy source and build
COPY . .
RUN npm run build

# Production image with nginx
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF

# Create nginx config
cat > nginx.conf << 'EOF'
server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
}
EOF
```

#### Docker Compose

```bash
# In project root
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    volumes:
      - ./backend/data:/app/data

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=http://localhost:8000
    depends_on:
      - backend
EOF
```

#### Deploy with Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## ⚙️ Environment Variables

### Backend (.env)

```bash
# Production
ENVIRONMENT=production
PYTHONUNBUFFERED=1

# Optional: If using real OpenAI
# OPENAI_API_KEY=sk-your-key-here

# Database (if using PostgreSQL instead of SQLite)
# DATABASE_URL=postgresql://user:pass@host:port/db
```

### Frontend (.env.production)

```bash
VITE_API_URL=https://your-backend-url.com
```

---

## 🔧 Backend Configuration

### Update CORS for Production

Edit `backend/app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

# Update origins for production
origins = [
    "http://localhost:5173",  # Local dev
    "https://convosage.vercel.app",  # Your production frontend
    "https://www.convosage.com",  # Custom domain if you have one
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🗄️ Database Options

### Option A: Keep SQLite (Simple)

✅ **Pros**: No setup, works immediately  
❌ **Cons**: Not ideal for multiple servers

Keep `backend/data/outlets.db` and deploy as-is.

### Option B: PostgreSQL (Production)

#### 1. Add PostgreSQL to Railway/Render

```bash
# Railway
railway add -d postgresql

# Render
# Add PostgreSQL database in dashboard
```

#### 2. Update Backend Code

```python
# backend/app/db/database.py
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./data/outlets.db"  # Fallback to SQLite
)

# Use PostgreSQL if available
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
```

#### 3. Migrate Data

```bash
# Export from SQLite
sqlite3 data/outlets.db .dump > outlets.sql

# Import to PostgreSQL
psql $DATABASE_URL < outlets.sql
```

---

## ✅ Pre-Deployment Checklist

### Code Preparation
- [ ] All tests passing (`pytest tests/`)
- [ ] No `TODO` comments in code
- [ ] Environment variables documented
- [ ] CORS origins updated for production
- [ ] Error messages don't expose internals
- [ ] Rate limiting configured

### Security
- [ ] No secrets in repository
- [ ] `.env` files in `.gitignore`
- [ ] SQL injection prevention tested
- [ ] XSS prevention in place
- [ ] HTTPS enforced
- [ ] Rate limiting active

### Performance
- [ ] Frontend bundle optimized
- [ ] Images compressed
- [ ] Database indexed
- [ ] Caching headers set
- [ ] Gzip compression enabled

### Monitoring
- [ ] Health check endpoint working
- [ ] Error logging configured
- [ ] Uptime monitoring (UptimeRobot)
- [ ] Performance monitoring (optional)

---

## 🧪 Testing Deployment

### 1. Test Backend

```bash
# Health check
curl https://your-backend-url.com/health

# API docs
open https://your-backend-url.com/docs

# Test chat endpoint
curl -X POST https://your-backend-url.com/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### 2. Test Frontend

1. Open `https://your-frontend-url.com`
2. Send a message
3. Test calculator: `/calc 5 + 3`
4. Test products: `/products tumbler`
5. Test outlets: `/outlets KL`
6. Refresh page - messages should persist
7. Test on mobile device

### 3. Load Testing

```bash
# Install hey
go install github.com/rakyll/hey@latest

# Test backend
hey -n 1000 -c 10 https://your-backend-url.com/health
```

---

## 📊 Monitoring Setup

### Render/Railway Built-in

Both platforms provide:
- Automatic health checks
- Request logs
- Resource usage metrics
- Deployment history

### External Monitoring (Optional)

#### UptimeRobot (Free)

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Add monitor for `https://your-backend-url.com/health`
3. Set alert email
4. Monitor every 5 minutes

#### Sentry (Error Tracking)

```bash
# Install
pip install sentry-sdk[fastapi]

# Configure in main.py
import sentry_sdk
sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

---

## 🔄 CI/CD Pipeline (Optional)

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest tests/

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Render
        run: |
          # Trigger Render deployment
          curl -X POST https://api.render.com/deploy/...

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          cd frontend
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## 🌐 Custom Domain (Optional)

### Backend

1. Buy domain (e.g., `api.convosage.com`)
2. In Render/Railway:
   - Go to Settings → Custom Domain
   - Add `api.convosage.com`
   - Update DNS with CNAME record

### Frontend

1. Use domain (e.g., `convosage.com`)
2. In Vercel:
   - Settings → Domains
   - Add `convosage.com`
   - Update DNS records

---

## 🐛 Troubleshooting

### Backend Not Starting

```bash
# Check logs
railway logs
# or
render logs

# Common issues:
# 1. Port binding - ensure using $PORT from env
# 2. Dependencies - check requirements.txt
# 3. Database - verify data/outlets.db exists
```

### Frontend Can't Connect

```bash
# Check CORS settings in backend
# Verify VITE_API_URL is correct
# Test backend URL directly

curl https://your-backend-url.com/health
```

### Database Issues

```bash
# SQLite permissions
chmod 644 data/outlets.db

# PostgreSQL connection
psql $DATABASE_URL -c "SELECT COUNT(*) FROM outlets;"
```

---

## 💰 Cost Estimates

### Free Tier Options

| Service | Plan | Cost | Limits |
|---------|------|------|--------|
| **Render** | Free | $0 | 750 hrs/month, sleeps after 15min |
| **Railway** | Free | $0 | $5 credit/month, ~100hrs |
| **Vercel** | Hobby | $0 | 100GB bandwidth |
| **Netlify** | Free | $0 | 100GB bandwidth |

### Paid Options (for production)

| Service | Plan | Cost/month |
|---------|------|------------|
| **Render** | Starter | $7 |
| **Railway** | Developer | $5 |
| **Vercel** | Pro | $20 |

**Estimated Total**: $7-12/month for hobby project

---

## 📈 Performance Optimization

### Backend

```python
# Add caching
from functools import lru_cache

@lru_cache(maxsize=100)
def get_products():
    # Cache product searches
    pass

# Enable gzip
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Frontend

```javascript
// Lazy load components
const ChatWindow = lazy(() => import('./components/ChatWindow'));

// Image optimization
// Use WebP format
// Add loading="lazy" to images

// Bundle optimization
// vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom']
        }
      }
    }
  }
}
```

---

## ✅ Post-Deployment

### 1. Verify Everything Works

- [ ] Backend health check responds
- [ ] Frontend loads
- [ ] Chat functionality works
- [ ] Calculator tool works
- [ ] Product search works
- [ ] Outlet search works
- [ ] Mobile view works
- [ ] HTTPS enabled
- [ ] CORS working

### 2. Share URLs

```
Backend API: https://convosage-api.onrender.com
Frontend App: https://convosage.vercel.app
API Docs: https://convosage-api.onrender.com/docs
```

### 3. Monitor for 24 Hours

- Check logs for errors
- Monitor response times
- Test from different locations
- Verify uptime

---

## 📝 Deployment Submission

When submitting to Mindhive, include:

```
✅ Live Backend URL: https://...
✅ Live Frontend URL: https://...
✅ API Documentation: https://.../docs
✅ GitHub Repository: https://github.com/.../convo-sage
✅ Test Credentials: (if applicable)
✅ Demo Video: (optional)
```

---

**Ready to deploy? Let me know which option you'd like to use!** 🚀

