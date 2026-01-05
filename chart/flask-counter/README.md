# Helm Chart – Flask Counter App

This directory contains the **Helm chart** used to deploy the Flask Counter application to Kubernetes.

Helm is the **supported and current deployment mechanism** for this project (Phase 3).



## 📦 Chart Overview

- Chart name: `flask-counter`
- Deploys the Flask Counter application


## ⚙️ Configuration

Key values exposed by the chart:

| Value | Description |
|------|-------------|
| `image.repository` | Docker image repository |
| `image.tag` | Docker image tag (immutable SHA) |
| `service.port` | Service port exposed inside the cluster |

Defaults and additional options can be found in [values.yaml](values.yaml).



## 📦 Chart Distribution

The packaged chart is published and maintained in the following repository:

- https://github.com/gal-halevi/helm-charts
