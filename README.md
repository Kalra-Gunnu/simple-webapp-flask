
# Flask CI/CD Pipeline with GitHub Actions & AWS EC2  

A **fully automated CI/CD pipeline** for a Flask application using **GitHub Actions**, Docker, and AWS EC2 for **Staging** and **Production** deployments.

---

## 📚 Table of Contents  

1. [Overview](#overview)  
2. [Architecture](#architecture)  
3. [Workflow Summary](#workflow-summary)  
4. [Step-by-Step Setup](#step-by-step-setup)  
   - [1. Fork the Repository](#1-fork-the-repository)  
   - [2. Create a Staging Branch](#2-create-a-staging-branch)  
   - [3. Add Basic Tests](#3-add-basic-tests)  
   - [4. Create GitHub Actions Workflow](#4-create-github-actions-workflow)  
   - [5. Disable Actions Temporarily](#5-disable-actions-temporarily)  
   - [6. Launch AWS EC2 Instances](#6-launch-aws-ec2-instances)  
   - [7. Configure GitHub Secrets](#7-configure-github-secrets)  
   - [8. Clone Repo Locally & Switch Branch](#8-clone-repo-locally--switch-branch)  
   - [9. Update Application for Environment Awareness](#9-update-application-for-environment-awareness)  
   - [10. Update Dockerfile](#10-update-dockerfile)  
   - [11. Update CI/CD Workflow](#11-update-cicd-workflow)  
   - [12. Push Changes to Staging](#12-push-changes-to-staging)  
   - [13. First Workflow Run](#13-first-workflow-run)  
   - [14. Fix Deployment Issue](#14-fix-deployment-issue)  
   - [15. Successful Staging Deployment](#15-successful-staging-deployment)  
   - [16. Deploy Production](#16-deploy-production)  
   - [17. Verify Production](#17-verify-production)  
5. [Secrets Required](#secrets-required)  
6. [Pipeline Trigger Rules](#pipeline-trigger-rules)  
7. [Final Status](#final-status)  
8. [Summary](#summary)  

---

## 🔎 Overview  

This pipeline automates the **build, test, and deployment** of a Flask app:  

✅ **Push to Staging branch** → Deploys to Staging EC2  
✅ **GitHub Release** → Deploys to Production EC2  
✅ **Dockerized Application** → Same build runs across both environments  
✅ **Secure Secrets** → Stored in GitHub Actions Secrets  

---

## 🏗 Architecture  

```
Developer Push → GitHub Actions → Docker Build & Test → Deploy via SSH → EC2 Container
```

- **GitHub Repo** → Source Code & Workflow  
- **GitHub Actions** → CI/CD Orchestration  
- **Docker** → App Packaging  
- **AWS EC2** → Hosting for Staging & Production  

---

## 🔄 Workflow Summary  

- **staging branch push** → Triggers Staging Build & Deploy  
- **release tag** → Triggers Production Build & Deploy  
- Test cases ensure stability before deployment  
- Environment variables differentiate Staging vs Production  

---

## ✅ Step-by-Step Setup  

### 1. Fork the Repository  
Fork the [original repo](https://github.com/mmumshad/simple-webapp-flask) into your GitHub account.  

![Forking Repo](screenshots/1.png)  
![Repo Forked](screenshots/2.png)  

---

### 2. Create a Staging Branch  
Create a new `staging` branch from `master`.  

![Creating Branch](screenshots/3.png)  
![Branch Created](screenshots/4.png)  

---

### 3. Add Basic Tests  
Added `tests/test_app.py` for simple Flask route verification.  

![Adding Tests](screenshots/5.png)  
![Tests Created](screenshots/6.png)  

---

### 4. Create GitHub Actions Workflow  
Created `.github/workflows/ci-cd.yml` to define build, test & deploy stages.  

![Creating Workflow](screenshots/7.png)  
![Workflow Created](screenshots/8.png)  

---

### 5. Disable Actions Temporarily  
Paused Actions initially until secrets were configured.  

---

### 6. Launch AWS EC2 Instances  
Created **2 Ubuntu EC2 instances**: one for Staging, one for Production.  

![EC2 Instances Running](screenshots/9.png)  

---

### 7. Configure GitHub Secrets  
In **Repo Settings → Secrets & Variables → Actions** added:  

| Secret          | Purpose                  |
|-----------------|--------------------------|
| `SSH_KEY`       | Private key for EC2 SSH  |
| `STAGING_HOST`  | Staging EC2 Public IP    |
| `STAGING_USER`  | SSH user for Staging     |
| `PROD_HOST`     | Production EC2 Public IP |
| `PROD_USER`     | SSH user for Production  |

![Configured Secrets](screenshots/10.png)  

---

### 8. Clone Repo Locally & Switch Branch  
```bash
git clone <repo_url>
cd simple-webapp-flask
git checkout staging
```
Opened repo in VS Code for updates.  

![Cloned Repo](screenshots/11.png)  
![Checked Branch](screenshots/12.png)  

---

### 9. Update Application for Environment Awareness  
Modified `app.py` to return messages based on `APP_ENV` (Staging/Production).  

![Updated app.py](screenshots/13.png)  

---

### 10. Update Dockerfile  
Added `ENV APP_ENV` with default Staging.  

![Updated Dockerfile](screenshots/14.png)  

---

### 11. Update CI/CD Workflow  
Modified `ci-cd.yml` → added `-e APP_ENV` in docker run.  

![Updated Workflow](screenshots/15.png)  

---

### 12. Push Changes to Staging  
```bash
git add .
git commit -m "Environment-aware app + Dockerfile update"
git push origin staging
```
Triggered **Staging Workflow**.  

![Push Changes](screenshots/16.png)  
![Workflow Triggered](screenshots/17.png)  

---

### 13. First Workflow Run  
✅ Build + Test Passed  
❌ Deployment failed (docker permission issue).  

![Failed Deployment](screenshots/18.png)  

---

### 14. Fix Deployment Issue  
Added `sudo` for docker commands → pushed → retriggered workflow.  

![Fixed Issue](screenshots/19.png)  

---

### 15. Successful Staging Deployment  
Deployed Flask container to staging:  

```
http://<STAGING_IP>:5000/how%20are%20you
✅ Shows: Hello from Staging environment!
```  

![Staging Success 1](screenshots/20.png)  
![Staging Success 2](screenshots/21.png)  
![Staging Success 3](screenshots/22.png)  

---

### 16. Deploy Production  
1. **GitHub → Releases → Draft new release**  
2. Select `master` branch → Tag `v1.0.0`  
3. Publish Release → triggers **Production Workflow**  
4. Fixed branch name (main → master) → retriggered → SUCCESS  

![Draft Release](screenshots/23.png)  
![Prod Workflow](screenshots/24.png)  
![Prod Success](screenshots/25.png)  

---

### 17. Verify Production  
```
http://<PRODUCTION_IP>:5000/how%20are%20you
✅ Shows: Hello from Production environment!
```  

![Production Verified](screenshots/26.png)

---

## 🔑 Secrets Required  

| Secret          | Description |
|-----------------|-------------|
| `SSH_KEY`       | Private SSH key for EC2 |
| `STAGING_HOST`  | Staging EC2 Public IP |
| `STAGING_USER`  | SSH User for Staging |
| `PROD_HOST`     | Production EC2 Public IP |
| `PROD_USER`     | SSH User for Production |

---

## 🏗 Pipeline Trigger Rules  

- **Push to `staging` branch** → Deploys to Staging Server  
- **GitHub Release on `master` branch** → Deploys to Production Server  

---

## ✅ Final Status  

✅ **Staging Deployment → Working**  
✅ **Production Deployment → Working**  
✅ **Automated Tests → Passing**  
✅ **CI/CD Workflow → Fully Functional**  

---

## 📜 Summary  

This CI/CD setup ensures:  

✔ Automated testing & validation  
✔ Seamless deployment to staging & production  
✔ Reproducible environment with Docker  
✔ Secure deployment using GitHub Secrets  

---