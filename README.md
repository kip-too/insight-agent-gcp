# Insight-Agent GCP Deployment

A secure, scalable, and automated production-ready FastAPI service for text analysis, deployed on Google Cloud Platform using Infrastructure as Code (Terraform) and CI/CD automation.

## 📋 Table of Contents
- [Architecture Overview](#architecture-overview)
- [Design Decisions](#design-decisions)
- [Windows Setup Guide](#windows-setup-guide)
- [Local Development](#local-development)
- [GCP Deployment](#gcp-deployment)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│  GitHub Actions  │───▶│  Cloud Build    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Terraform     │◀───│  Infrastructure  │───▶│ Artifact Registry│
│   (IaC)         │    │   Provisioning   │    │   (Docker)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │   Cloud Run     │
                                               │   (FastAPI)     │
                                               │  Internal-Only  │
                                               └─────────────────┘
```

**GCP Services Used:**
- **Cloud Run**: Serverless container platform for the FastAPI application
- **Artifact Registry**: Secure Docker image storage
- **Cloud Build**: CI/CD automation (triggered by GitHub Actions)
- **IAM**: Identity and access management with least-privilege service accounts

## 🎯 Design Decisions

### Why Cloud Run?
- **Serverless**: Auto-scaling from 0 to N instances based on demand
- **Cost-effective**: Pay only for actual usage, perfect for variable workloads
- **Container-native**: Easy deployment of containerized applications
- **Built-in security**: Integrated with GCP IAM and VPC

### Security Implementation
- **Internal-only traffic**: Cloud Run service configured with `INGRESS_TRAFFIC_INTERNAL_ONLY`
- **Least-privilege IAM**: Dedicated service account with minimal required permissions
- **Non-root container**: Application runs as non-root user
- **Secrets management**: No hardcoded credentials; uses GCP service account authentication

### CI/CD Pipeline
- **Multi-stage pipeline**: Lint/Test → Build → Deploy
- **Infrastructure as Code**: Terraform manages all GCP resources
- **Automated deployments**: Triggered on pushes to main branch
- **Container security**: Slim base images and security scanning

## 🪟 Windows Setup Guide

### Prerequisites Installation

#### 1. Install Required Software

**Python 3.11+**
1. Download from [python.org](https://www.python.org/downloads/windows/)
2. ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation
3. Verify: `python --version` and `pip --version`

**Git**
1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Use default installation settings
3. Verify: `git --version`

**Docker Desktop**
1. Download from [docker.com](https://www.docker.com/products/docker-desktop/)
2. Install and restart your computer
3. Start Docker Desktop and wait for it to fully load
4. Verify: `docker --version`

**Google Cloud CLI**
1. Download from [Google Cloud SDK](https://cloud.google.com/sdk/docs/install#windows)
2. Run the installer and follow prompts
3. Verify: `gcloud --version`

**Terraform**
1. Download from [terraform.io](https://www.terraform.io/downloads)
2. Extract to a folder (e.g., `C:\terraform`)
3. Add the folder to your PATH environment variable
4. Verify: `terraform --version`

**VS Code**
1. Download from [code.visualstudio.com](https://code.visualstudio.com/)
2. Install recommended extensions:
   - Python (Microsoft)
   - Terraform (HashiCorp)
   - Docker (Microsoft)
   - YAML (Red Hat)

### 2. Project Setup

#### Clone or Create Project
```cmd
# Option 1: Clone existing repository
git clone https://github.com/kip-too/insight-agent-gcp.git
cd insight-agent-gcp

# Option 2: Create new project
mkdir C:\Projects\insight-agent-gcp
cd C:\Projects\insight-agent-gcp
git init
```

#### Create Project Structure
```cmd
mkdir app terraform .github .github\workflows scripts .vscode
type nul > README.md
type nul > .gitignore
# ... create other files as needed
```

#### Open in VS Code
```cmd
code .
```

### 3. Set Up Python Environment

```cmd
# Navigate to app directory
cd app

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows CMD)
venv\Scripts\activate

# For PowerShell users:
# venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## 💻 Local Development

### Quick Start

1. **Activate Virtual Environment:**
   ```cmd
   cd app
   venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```cmd
   python main.py
   ```

4. **Access the API:**
   - API Docs: http://localhost:8080/docs
   - Health Check: http://localhost:8080/health
   - Main Endpoint: http://localhost:8080/analyze

### Development Workflow

#### Running Locally
```cmd
# Start development server
cd app
venv\Scripts\activate
python main.py

# Or use uvicorn directly with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

#### Testing with curl (CMD)
```cmd
# Health check
curl http://localhost:8080/health

# Analyze text
curl -X POST "http://localhost:8080/analyze" ^
     -H "Content-Type: application/json" ^
     -d "{\"text\": \"I love cloud engineering!\"}"
```

#### Testing with PowerShell
```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8080/health" -Method Get

# Analyze text
$body = @{text = "I love cloud engineering!"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8080/analyze" -Method Post -Body $body -ContentType "application/json"
```

#### Docker Testing
```cmd
# Build image
docker build -t insight-agent ./app

# Run container
docker run -p 8080:8080 insight-agent

# Test container
curl http://localhost:8080/health
```

### VS Code Configuration

Create `.vscode\settings.json`:
```json
{
    "python.defaultInterpreterPath": "./app/venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "files.exclude": {
        "**/__pycache__": true,
        "**/venv": false
    }
}
```

Create `.vscode\launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/app/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/app",
            "env": {
                "PORT": "8080"
            }
        }
    ]
}
```

## ☁️ GCP Deployment

### 1. GCP Setup

#### Authenticate with GCP
```cmd
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

#### Enable Billing
Ensure billing is enabled for your project at: https://console.cloud.google.com/billing

### 2. Configure Terraform

#### Create terraform.tfvars
```cmd
cd terraform
copy terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars`:
```hcl
project_id = "your-gcp-project-id"
region     = "us-central1"
image_tag  = "latest"
```

#### Deploy Infrastructure
```cmd
cd terraform

# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply changes
terraform apply
```

### 3. GitHub Actions Setup

#### Create Service Account for CI/CD
```cmd
# Create service account
gcloud iam service-accounts create github-actions-sa --display-name="GitHub Actions SA"

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member="serviceAccount:github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" --role="roles/run.admin"
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID --member="serviceAccount:github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" --role="roles/artifactregistry.admin"

# Create key
gcloud iam service-accounts keys create key.json --iam-account=github-actions-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

#### Configure GitHub Secrets
Add these secrets to your GitHub repository:
- `GCP_PROJECT_ID`: Your GCP project ID
- `GCP_SA_KEY`: Contents of the `key.json` file

### 4. Deploy via CI/CD

Push to main branch to trigger deployment:
```cmd
git add .
git commit -m "Initial deployment"
git push origin main
```

## 📚 API Documentation

### Endpoints

#### `GET /`
Returns service information and version.

**Response:**
```json
{
  "message": "Insight-Agent API is running",
  "version": "1.0.0"
}
```

#### `GET /health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy"
}
```

#### `POST /analyze`
Analyzes the provided text and returns statistics.

**Request Body:**
```json
{
  "text": "Your text to analyze here"
}
```

**Response:**
```json
{
  "original_text": "Your text to analyze here",
  "word_count": 5,
  "character_count": 26,
  "sentence_count": 1,
  "analysis_metadata": {
    "has_uppercase": true,
    "has_numbers": false,
    "unique_words": 5,
    "avg_word_length": 4.2
  }
}
```

### Testing in Production

Since the Cloud Run service is configured for internal-only access, test from within GCP:

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe insight-agent --region=us-central1 --format="value(status.url)")

# Test from Cloud Shell
curl -X POST "$SERVICE_URL/analyze" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -d '{"text": "Hello from GCP!"}'
```

## 📁 Project Structure

```
insight-agent-gcp/
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── app/                     # FastAPI application
│   ├── main.py             # Main application code
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container configuration
├── terraform/               # Infrastructure as Code
│   ├── main.tf            # Main Terraform configuration
│   ├── variables.tf       # Variable definitions
│   ├── outputs.tf         # Output definitions
│   └── terraform.tfvars.example  # Example variables
├── .github/                 # GitHub Actions
│   └── workflows/
│       └── ci-cd.yml       # CI/CD pipeline
├── scripts/                 # Helper scripts
│   └── setup.bat          # Windows setup script
└── .vscode/                # VS Code configuration
    ├── settings.json      # Editor settings
    └── launch.json        # Debug configuration
```

## 🤝 Contributing

### Development Process
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and test locally
3. Run linting: `black app/` and `flake8 app/`
4. Commit changes: `git commit -m "Add your feature"`
5. Push branch: `git push origin feature/your-feature`
6. Create pull request

### Code Standards
- Use Black for Python formatting
- Follow PEP 8 guidelines
- Add type hints where possible
- Write descriptive commit messages
- Include tests for new features

## 🐛 Troubleshooting

### Common Windows Issues

#### "Python not found"
**Solution:** Reinstall Python ensuring "Add to PATH" is checked during installation.

#### Virtual environment activation fails
**Solution:** Use full path: `C:\path\to\project\app\venv\Scripts\activate`

#### Docker commands fail
**Solution:** 
1. Start Docker Desktop
2. Wait for it to fully initialize
3. Check Docker is running: `docker ps`

#### Port 8080 already in use
**Solutions:**
1. Change port in `main.py`: `uvicorn.run(app, host="0.0.0.0", port=8081)`
2. Kill process using port: `netstat -ano | findstr :8080` then `taskkill /PID <PID> /F`

#### Module not found errors
**Solution:** Ensure virtual environment is activated before running:
```cmd
cd app
venv\Scripts\activate
python main.py
```

### GCP Issues

#### Authentication errors
**Solutions:**
1. Login again: `gcloud auth login`
2. Set project: `gcloud config set project YOUR_PROJECT_ID`
3. Check permissions: `gcloud auth list`

#### Terraform state issues
**Solutions:**
1. Initialize: `terraform init`
2. Refresh state: `terraform refresh`
3. If corrupted: Delete `.terraform` folder and re-init

#### Cloud Run deployment fails
**Check:**
1. Billing is enabled
2. Required APIs are enabled
3. Service account has proper permissions
4. Docker image exists in Artifact Registry

### Application Issues

#### FastAPI server won't start
**Check:**
1. Virtual environment is activated
2. All dependencies are installed: `pip install -r requirements.txt`
3. Port is available
4. Python version compatibility (3.11+)

#### API returns 500 errors
**Debug:**
1. Check application logs
2. Verify input data format
3. Test with simple input
4. Check error messages in response

## 📊 Monitoring and Maintenance

### Local Monitoring
- **Logs**: Check terminal output where the app is running
- **Health**: Visit http://localhost:8080/health
- **Metrics**: Use FastAPI's built-in `/docs` endpoint

### Production Monitoring
- **Logs**: View in Cloud Logging console
- **Metrics**: Monitor in Cloud Monitoring
- **Costs**: Track in Cloud Billing console
- **Health**: Monitor `/health` endpoint

### Updates and Maintenance
- **Dependencies**: Regularly update `requirements.txt`
- **Security**: Monitor for security advisories
- **Infrastructure**: Review and update Terraform configurations
- **Monitoring**: Set up alerts for errors and performance

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues and questions:
1. Check this README for solutions
2. Review GitHub Issues
3. Check application logs in VS Code or Cloud Logging
4. Verify all prerequisites are installed and configured
5. Ensure GCP billing is enabled and APIs are activated

