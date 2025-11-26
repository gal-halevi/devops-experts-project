# Counter App – Flask (Application & Docker Guide)

This folder contains the Flask application and Dockerfile used to containerize it.

### The application exposes:

- `/` → increments counter & returns value (main homepage)
- `/count` → returns current counter value without changing it
- `/inc` → increments counter explicitly via POST 
- `/healthz` → liveness probe
- `/readyz` → readiness probe  
- `/admin/reset` → admin-protected counter reset endpoint  

### Environment variables:

| Name          | Required? | Purpose                                            | Default                |
|---------------|-----------|----------------------------------------------------|------------------------|
| `COUNTER_PATH`  | optional  | Path for storing counter file                      | /data/counter.txt      |
| `ADMIN_TOKEN`   | required  | Token for accessing `/admin/reset`                   | none (must be set)     |

---

# 📦 1. Build the Docker Image

You can choose any tag you like:

```bash
docker build -t counter-app:<tag> .
```

Examples:

```bash
docker build -t counter-app:1.0 .
docker build -t counter-app:latest .
```

---

# ▶️ 2. Run the Container Locally

```bash
docker run -p 5000:5000 \
  -e COUNTER_PATH=/data/counter.txt \
  -e ADMIN_TOKEN=super-duper-secret \
  -v $(pwd)/data:/data \
  counter-app:<tag>
```

### Why use `-v`?

It mounts a host directory into the container so the counter file persists:

- Without `-v`, each restart resets the counter  
- With `-v`, the file is stored in `./data/` on your local machine  

You may omit the volume if persistence is not needed.

---

# 🧪 3. Test the App

```bash
curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/count
curl -X POST http://127.0.0.1:5000/inc
```

Admin reset:

```bash
curl -X POST \
  -H "X-Admin-Token: super-duper-secret" \
  http://127.0.0.1:5000/admin/reset
```

---

# 📚 For Kubernetes deployment

See the documentation in:

👉 `../k8s/README.md`

