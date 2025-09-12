# **GitLab CI(for a simple Python Web Application) and GitOps FluxCD Principle(for automated rollout in kind cluster)**

# **Overview**
This project demonstrates a GitOps-based CI/CD pipeline using two separate repositories:
# **app-repo**
   1. Contains application source code, Dockerfile, and GitLab CI pipeline.
   2. Builds and publishes container images to a registry.
   3. Basic Unit Test Execution.
# **gitops-repo**
   1. Contains Kubernetes manifests file (or Helm charts).
   2. Defines how the application is deployed in the cluster.
   3. Watched by FluxCD, which reconciles changes automatically.
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
```

# **CI/CD Pipeline Workflow**
The .gitlab-ci.yml file defines the following stages:

# **Build:**
   1. Builds a Docker image of the Flask application.
   2. Tags the image with the short commit SHA or anything which is suitable for you choose tagging as per your need.
   3. Pushes the tagged image to the GitLab Container Registry.
# **Test:**
   1. Installs Python dependencies.
   2. Runs unit tests using pytest to ensure the application code is working correctly.
# **Deploy (GitOps Trigger):**
   1. Clones the gitops-repo.
   2. Updates the deployment.yaml manifest file with the new Docker image tag built in the build stage.
   3. Commits and pushes the change to the gitops-repo.

# **Bootstrap gitops-repo** : Repo created by Flux CLI command not manually from Gitlab GUI which is explained below Step#4
I kept it simple: a plain Kustomize overlay that points to the app deployment. we could also store a Helm chart; the same sed replacement works on values.yaml & other stuff.
```
.
gitops-repo/
├─ clusters/
│   └─ kind/
         └─ flux-system
                 └─ kustomization.yaml                 
└─ apps/
    └─ myapp/
         ├─ kustomization.yaml
         └─ deployment.yaml
```

# 1️⃣ Create a Kind cluster (we can name it anything)
```kind create cluster --name flux-demo```

# 2️⃣ Set KUBECONFIG to talk to the new cluster - Optional for my environment doesn't need that.
```export KUBECONFIG="$(kind get kubeconfig-path --name flux-demo)"```

# 3️⃣ Install Flux Operator &  CLI (if you haven't already)
     helm install flux-operator oci://ghcr.io/controlplaneio-fluxcd/charts/flux-operator 
     curl -s https://fluxcd.io/install.sh | sudo bash 
     kubectl apply -f https://github.com/fluxcd/flux2/releases/latest/download/install.yaml 

# 4️⃣ Bootstrap Flux – this creates the Flux system namespace, registers the gitops repo, and sets up a Kustomization that watches clusters/kind/kustomization.yaml
`flux bootstrap gitlab \
  --owner=YOUR_GROUP \
  --repository=gitops-repo \
  --branch=main \
  --path=clusters/kind \
  --personal  # omit if you use a group‑level token `
  
# 5️⃣ Should show the git repository object
```kubectl -n flux-system get gitrepositories```

# 6️⃣ Should show the kustomization object (and its status = Ready)
```kubectl -n flux-system get kustomizations```
If you see a 'Ready and Reconciled' status, Flux is now watching the gitops-repo.

# **E2E Flow Validation & Verification**
   * **Push a change to app-repo (e.g., edit src/app.py or anything which you want)**
   * **GitlabCI will trigger and does three things (Docker Image builder/Pushing Image to registry/Unit Test Execution & Update gitops-repo's deployment.yaml with the new tag and push it.**
   * **Flux detects the change verify by**: ```kubectl -n flux-system get kustomizations -w```
   * **Verify pods run with new image**: ```kubectl get po -n <<your namespace>>```
   * **Test the Endpoints**: ```kubectl port-forward svc/myapp 8083/8080:80 & curl http://localhost:8080/3/healthz```

# **Few Points to Remember**
* Slave Machine type or Gitlab Runner matters a lot if you choose Docker Type or K8S executor or shell based please consider this, have tried with Docker/Shell and this solution will work on both.
* Use Gitlab CI/CD variable or any other valut mechanism to restore your key information like USERNAME/PW/IP & other stuff.
* This demonstrates on-a single control plane k8s created via kind & on top of that flux operator/controller has been installed and then repo reconcilltion starts via kustomizations.
* Binaries dependencies should be taken care of.

# **How AI Assistance helped me in this project**
Artificial Intelligence is no longer just a buzzword; it has become a true automation and efficiency lever across domains, enabling individuals and teams to achieve their milestones faster.
In my case, AI has been instrumental in generating application code, even scaffolding CI pipeline definitions. While adjustments were required to make them production-ready, the overall process was significantly accelerated.
In short, AI has increased operational efficiency, reduced lead time, and improved project delivery speed. that's my 2cents on this subject.

Happy Learning!!!🚀
