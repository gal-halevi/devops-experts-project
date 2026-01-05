# Counter App – Flask · Docker · Kubernetes

A minimal Flask-based counter service used to demonstrate containerization and Kubernetes concepts:

- Containerizing a Python Flask application using Docker
- Deploying the application to a Kubernetes cluster (Minikube)
- Using ConfigMaps, Secrets, Deployments, Services, Liveness/Readiness, CronJobs, and HPA


---

## 📁 Repository Structure

```
.
├── app/                 # Flask application + Dockerfile
│   └── README.md        # How to build/run the Docker image locally
│
├── k8s/                 # Kubernetes manifests
│   └── README.md        # How to deploy the app on Minikube
└── README.md            # High-level overview (this file)
```

---



## 📝 Important Notes

For learning purposes and for the sake of simplicity I decided to use
### ⚠️ File-Based Counter



This approach is **not concurrency-safe**, **not persistent across Pods**, and **not production-grade**.  


### ⚠️ Secret.yaml pushed to Git

This isn't best practice to say the least, and should be avoided.
Secrets should be created with `kubectl create secret` or a secrets manager

---

## 📚 Further Documentation

- **App + Docker build and run instructions:**  
  👉 [src/README.md](src/README.md)

- **Kubernetes deployment instructions:**  
  👉 [k8s/README.md](k8s/README.md)


## Git Workflow

This project follows a feature-branch workflow:

- `main` is always deployable
- All changes are developed in feature branches
- Pull Requests are used for integration
- CI pipelines validate changes before merging

Branch naming:
- `feature/*` – new functionality
- `bugfix/*` – non-urgent fixes
- `hotfix/*` – urgent production fixes
