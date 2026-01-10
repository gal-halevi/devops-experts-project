# DevOps Experts – Final Project (Phase 3)

This repository contains a DevOps learning project focused on building a complete CI/CD flow:

- Application testing
- Docker image build & push
- Deployment to a local Kubernetes cluster using Helm

The goal of **Phase 3** is to establish a solid, reproducible pipeline that can later be extended to deploy into a cloud-managed Kubernetes cluster with minimal changes.

---

## 📁 Repository Structure

```
.
├── Jenkinsfile            # CI/CD pipeline definition
├── src/                   # Application source code
├── tests/                 # Pytest-based test suite
├── chart/                 # Helm chart (source of truth for deployment)
├── k8s/                   # Deprecated raw Kubernetes manifests (reference)
└── README.md              # Project overview (this file)
```

---

## 🔄 CI/CD Pipeline Overview

The project uses a **Jenkins Multibranch Pipeline**.

### Pipeline behavior by branch

| Branch         | Tests | Build Image | validate & push Image              | Deploy |
|----------------|-------|-------------|-------------------------|--------|
| feature/bugfix branch | ✅    | ✅          | ✅ (SHA tag)            | ❌     |
| main branch    | ✅    | ✅          | ✅ (SHA + latest)       | ✅     |

### Key points

- Docker images are always tagged with an immutable `sha-<commit>` tag
- The `latest` tag is pushed **only** from the `main` branch
- Feature branches are used for validation and iteration

---

## 🧰 Jenkins Agent Requirements

The pipeline is designed to run on a **single Jenkins agent**, executing all stages locally.

The Jenkins agent must have the following tools installed:
- Java (OpenJDK 11 or newer)
- Python 3
- Docker (with permission to access the daemon)
- Helm
- kubectl
- Access to a local Kubernetes cluster (for example: minikube)
- A configured kubeconfig context pointing to the local cluster

---

## ☸️ Kubernetes Deployment (Phase 3)

Deployment is performed using **Helm** against a **local Kubernetes cluster**.

The pipeline deploys the application using:

```bash
helm upgrade --install counter-app gal-halevi-helm/flask-counter \
  --version 0.2.0
  --set image.repository=<repository> \
  --set image.tag=sha-<commit>
```

Helm is the **supported and maintained deployment mechanism**.

For details, see:
- Helm chart documentation: [README.md](/chart/flask-counter/README.md)

---

## 🌿 Git Workflow

This project follows a feature-branch workflow:

- `main` is always deployable
- All changes are developed in short-lived feature branches and merged via Pull Requests
- CI validates changes on every branch before merging

Branch naming (optional convention):
- `feature/*` – new functionality
- `bugfix/*` – non-urgent fixes
- `hotfix/*` – urgent fixes

---

## 📚 Further Documentation

- Application and Docker usage: [/src/README.md](/src/README.md)
- Helm chart details: [/chart/README.md](/chart/flask-counter/README.md)
- Raw Kubernetes manifests (reference only): [/k8s/README.md](/k8s/README.md)
