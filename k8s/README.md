# Counter App – Kubernetes Deployment Guide

This folder contains all Kubernetes manifests for deploying the Flask counter application on Minikube.

Manifests included:

- `deployment.yaml`
- `service.yaml`
- `configmap.yaml`
- `secret.yaml`
- `cronjob.yaml`
- `hpa.yaml`

⚠️ The `secret.yaml` in this folder is included only for educational purposes.  
In production, Secrets should never be committed to Git.

---

# 🏗 1. Start Minikube

```bash
minikube start
```

Enable metrics server (needed for HPA):

```bash
minikube addons enable metrics-server
```

Verify:

```bash
kubectl get pods -n kube-system | grep metrics
```

---

# 📁 2. Apply Manifests

```bash
cd k8s/
kubectl apply -f .
```

Check status:

```bash
kubectl get pods
kubectl get svc
kubectl get cronjobs
kubectl get hpa
```

---

# 🌐 3. Accessing the Application

Get Kubernetes URL for the service in your local cluster:
```bash
minikube service counter-app-service --url
```

Minikube will print a URL like: 
```bash
http://127.0.0.1:50168
```
Keep this terminal open (minikube is running a proxy).

**(Use the URL printed by Minikube in all examples below — replace it with your own value.)**

In another terminal, use the given URL:

```bash
curl http://127.0.0.1:50168/
curl http://127.0.0.1:50168/count
curl -X POST http://127.0.0.1:50168/inc
```

Admin reset:

```bash
curl -X POST \
  -H "X-Admin-Token: super-duper-secret" \
  http://127.0.0.1:50168/admin/reset
```

---

# 🔁 4. CronJob

The CronJob runs every minute and calls `/inc` on the service to auto-increment the counter.

View CronJobs and Jobs:

```bash
kubectl get cronjobs
kubectl get jobs
```

The CronJob limits history in its spec:

```yaml
successfulJobsHistoryLimit: 3
failedJobsHistoryLimit: 3
```

This prevents cluttering the cluster with old Jobs history.

---

# 📈 5. HPA – Auto Scaling

View the HPA:

```bash
kubectl get hpa
kubectl describe hpa counter-app-hpa
```

Generate load (from your host):

```bash
while true; do curl http://127.0.0.1:50168/ >/dev/null; done
```

Watch scaling:

```bash
kubectl get pods -w
kubectl get hpa -w
```

As CPU usage rises, the HPA should increase the number of replicas (within the configured min/max).

---

# 🧹 Cleanup

To delete all resources in this folder:

```bash
cd k8s/
kubectl delete -f .
```