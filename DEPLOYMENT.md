# Deployment Guide

## Deployment Options

### 1. Local Development (Already Covered)
See [QUICK_START.md](QUICK_START.md) for local setup.

---

## 2. Docker Deployment

### Prerequisites
- Docker installed
- Docker Compose installed
- Google Earth Engine authenticated

### Steps

1. **Authenticate Earth Engine** (on host machine):
```bash
earthengine authenticate
```

2. **Create `.env` file**:
```bash
SECRET_KEY=your-production-secret-key
GEE_PROJECT_ID=your-gee-project-id
```

3. **Build and run**:
```bash
docker-compose up -d
```

4. **Access application**:
```
http://localhost:5000
```

5. **View logs**:
```bash
docker-compose logs -f
```

6. **Stop application**:
```bash
docker-compose down
```

### Docker Commands

```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f app

# Restart services
docker-compose restart

# Remove all containers and volumes
docker-compose down -v
```

---

## 3. Cloud Deployment

### AWS Deployment

#### Option A: EC2 Instance

1. **Launch EC2 instance**:
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium (minimum)
   - Storage: 20GB
   - Security group: Allow ports 22, 80, 443, 5000

2. **Connect to instance**:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install dependencies**:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.10 python3-pip python3-venv -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

4. **Clone and setup project**:
```bash
git clone your-repo-url
cd land-cover-classifier
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Setup Earth Engine**:
```bash
earthengine authenticate
```

6. **Setup frontend**:
```bash
cd frontend
npm install
npm run build
cd ..
```

7. **Run with systemd**:

Create `/etc/systemd/system/landcover.service`:
```ini
[Unit]
Description=Land Cover Classifier
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/land-cover-classifier
Environment="PATH=/home/ubuntu/land-cover-classifier/venv/bin"
ExecStart=/home/ubuntu/land-cover-classifier/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable landcover
sudo systemctl start landcover
sudo systemctl status landcover
```

8. **Setup Nginx reverse proxy**:
```bash
sudo apt install nginx -y
```

Create `/etc/nginx/sites-available/landcover`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/landcover /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

9. **Setup SSL with Let's Encrypt**:
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

#### Option B: AWS Elastic Beanstalk

1. **Install EB CLI**:
```bash
pip install awsebcli
```

2. **Initialize EB**:
```bash
eb init -p python-3.10 land-cover-classifier
```

3. **Create environment**:
```bash
eb create production-env
```

4. **Deploy**:
```bash
eb deploy
```

5. **Open application**:
```bash
eb open
```

---

### Google Cloud Platform (GCP)

#### App Engine Deployment

1. **Create `app.yaml`**:
```yaml
runtime: python310
entrypoint: gunicorn -b :$PORT app:app

env_variables:
  FLASK_ENV: "production"
  SECRET_KEY: "your-secret-key"

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

2. **Deploy**:
```bash
gcloud app deploy
```

3. **View application**:
```bash
gcloud app browse
```

---

### Heroku Deployment

1. **Create `Procfile`**:
```
web: gunicorn app:app
```

2. **Create `runtime.txt`**:
```
python-3.10.12
```

3. **Deploy**:
```bash
heroku create your-app-name
git push heroku main
heroku open
```

4. **Set environment variables**:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set GEE_PROJECT_ID=your-project-id
```

---

## 4. Production Considerations

### Security

1. **Environment Variables**:
   - Never commit `.env` to git
   - Use secrets management (AWS Secrets Manager, etc.)

2. **HTTPS**:
   - Always use SSL/TLS in production
   - Use Let's Encrypt for free certificates

3. **API Rate Limiting**:
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)
```

4. **CORS Configuration**:
```python
CORS(app, origins=["https://your-domain.com"])
```

### Performance

1. **Use Gunicorn**:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Enable Caching**:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

3. **Use CDN** for frontend assets

4. **Database** for metadata (PostgreSQL, MongoDB)

### Monitoring

1. **Application Logs**:
```python
import logging

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

2. **Error Tracking** (Sentry):
```bash
pip install sentry-sdk
```

```python
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

3. **Performance Monitoring** (New Relic, DataDog)

### Backup

1. **Database backups** (if using database)
2. **Model backups** (trained models)
3. **Configuration backups**

### Scaling

1. **Horizontal Scaling**:
   - Multiple application instances
   - Load balancer

2. **Vertical Scaling**:
   - Increase instance size
   - More CPU/RAM

3. **Background Jobs**:
```bash
pip install celery redis
```

```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def process_imagery(bounds, dates):
    # Long-running task
    pass
```

---

## 5. Environment-Specific Configurations

### Development
```python
DEBUG = True
TESTING = True
```

### Staging
```python
DEBUG = False
TESTING = True
```

### Production
```python
DEBUG = False
TESTING = False
SECRET_KEY = os.environ['SECRET_KEY']
```

---

## 6. Health Checks

Add health check endpoint:
```python
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })
```

---

## 7. Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        run: |
          # Your deployment commands
```

---

## 8. Troubleshooting

### Common Issues

1. **Port already in use**:
```bash
lsof -ti:5000 | xargs kill -9
```

2. **Permission denied**:
```bash
sudo chown -R $USER:$USER /path/to/app
```

3. **Out of memory**:
   - Increase instance size
   - Optimize model loading
   - Use batch processing

4. **GEE authentication**:
```bash
earthengine authenticate --force
```

---

## 9. Maintenance

### Regular Tasks

1. **Update dependencies**:
```bash
pip install --upgrade -r requirements.txt
npm update
```

2. **Clean old files**:
```bash
find exports/ -mtime +30 -delete
find data/ -mtime +30 -delete
```

3. **Monitor disk space**:
```bash
df -h
```

4. **Check logs**:
```bash
tail -f logs/app.log
```

---

## 10. Cost Optimization

### AWS
- Use spot instances for non-critical workloads
- Auto-scaling based on demand
- S3 lifecycle policies for old data

### GCP
- Preemptible VMs
- Committed use discounts
- Cloud Storage lifecycle management

### General
- Cache frequently accessed data
- Optimize image processing
- Use smaller instance types when possible
- Clean up unused resources

---

## Support

For deployment issues:
1. Check logs first
2. Review error messages
3. Verify environment variables
4. Test API endpoints
5. Check network connectivity
6. Verify GEE authentication

---

## Production Checklist

- [ ] Environment variables configured
- [ ] HTTPS enabled
- [ ] Database backups configured
- [ ] Monitoring setup
- [ ] Error tracking enabled
- [ ] Rate limiting implemented
- [ ] CORS properly configured
- [ ] Logs rotation setup
- [ ] Health checks working
- [ ] Auto-scaling configured
- [ ] Security groups/firewall rules set
- [ ] Domain name configured
- [ ] SSL certificate installed
- [ ] Performance testing done
- [ ] Documentation updated
