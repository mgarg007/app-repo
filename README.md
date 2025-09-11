# **GitOps with GitLab CI and FluxCD & create a simple python web application**
 🔹Overview

This project demonstrates a GitOps-based CI/CD pipeline using two separate repositories:

app-repo

Contains application source code, Dockerfile, and GitLab CI pipeline.

Builds and publishes container images to a registry.

gitops-repo

Contains Kubernetes manifests (or Helm charts).

Defines how the application is deployed in the cluster.

Watched by FluxCD, which reconciles changes automatically.

By combining GitLab CI for CI (build & test) and FluxCD for CD (GitOps reconciliation), this solution ensures reliable, automated, and auditable deployments.

## **Repository Structure**

```
.
app-repo/
├── src/app.py           # Sample Python Web application
├── tests/test_app.py    # Basic unit test - related to /healthz only
├── requirements.txt     # Package installation for execution using pip
├── Dockerfile           # Build instructions
└── .gitlab-ci.yml       # GitLab CI pipeline
