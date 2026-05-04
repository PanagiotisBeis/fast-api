#  FastAPI CI/CD Pipeline (Jenkins + Docker + Ansible + AWS)

## Overview

This project demonstrates a complete **CI/CD pipeline** for deploying a Python FastAPI application using:

* Jenkins (CI/CD orchestration)
* Docker (containerization)
* Docker Hub (image registry)
* Ansible (deployment automation)
* AWS EC2 (infrastructure)

The pipeline automatically builds, pushes, and deploys a containerized application to a remote server.

---

## Architecture

```text
GitHub
   ↓
Jenkins (EC2)
   ↓
Docker Build
   ↓
Docker Hub
   ↓
Ansible (SSH)
   ↓
App EC2 (Docker Container)
```

---

## ⚙️ Tech Stack

* **Backend**: FastAPI (Python)
* **CI/CD**: Jenkins
* **Containerization**: Docker
* **Registry**: Docker Hub
* **Configuration Management**: Ansible
* **Cloud**: AWS EC2
* **Authentication**: SSH Keys & Jenkins Credentials

---

## Pipeline Stages

### 1. Git Checkout

Pulls the latest source code from GitHub.

### 2. Build Docker Image

Builds the FastAPI application into a Docker image.

### 3. Tag Image

Tags the image using a versioning strategy:

```text
1.0.<BUILD_NUMBER>
```

Also updates the `latest` tag.

### 4. Push to Docker Hub

Authenticates with Docker Hub and pushes:

* versioned image
* latest image

### 5. Deploy with Ansible

Jenkins triggers an Ansible playbook which:

* logs into Docker Hub on the target EC2
* pulls the latest image
* removes the previous container
* runs a new container
* exposes port 8000

### 6. Health Check

The deployment is validated using a `/health` endpoint with retry logic.

---

## Project Structure

```text
.
├── app/
├── Dockerfile
├── requirements.txt
├── Jenkinsfile
└── ansible/
    ├── inventory.ini
    └── deploy.yml
```

---

## Credentials Management

Sensitive data is **not stored in the repository**.

Managed securely via Jenkins:

* Docker Hub credentials
* SSH private key for EC2 access

---

## Deployment Flow

```text
1. Developer pushes code to GitHub
2. Jenkins pipeline is triggered
3. Docker image is built and tagged
4. Image is pushed to Docker Hub
5. Ansible connects to EC2 via SSH
6. New container is deployed
7. Health check validates deployment
```

---

## Concepts Demonstrated

* CI/CD pipeline design
* Infrastructure separation (CI server vs App server)
* Immutable deployments (container-based)
* Secure credential handling
* Automated remote deployment via Ansible
* Health check & retry mechanisms
* Versioned Docker images for rollback capability

---


## Future Improvements


* Add Terraform for infrastructure provisioning
* Add monitoring (Prometheus / Grafana)
* Implement rolling deployments 


---

## Author

Panagiotis Beis

