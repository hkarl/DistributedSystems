# Chapter 5 — Practical: How to Operate: Homework Assignments

---

### Homework 1 — Infrastructure as Code: Ansible

**Learning goal:** Experience the IaC philosophy hands-on; understand idempotency and
configuration drift.

**Tasks:**

1. **Manual setup vs. Ansible:**  On a fresh virtual machine (or a local Docker container
   running Ubuntu), manually install and start an nginx web server:
   ```bash
   apt-get install -y nginx
   systemctl start nginx
   ```
   Then write an Ansible playbook that achieves the same result.  Your playbook must:
   - Use `ansible.builtin.package` to install nginx
   - Use `ansible.builtin.service` to ensure nginx is started and enabled on boot
   - Use `ansible.builtin.copy` or `ansible.builtin.template` to deploy a custom
     `index.html`

2. **Idempotency test:** Run your playbook twice in a row against the same host.  Compare
   the output of both runs.
   - How many tasks show `changed` vs. `ok` on the second run?
   - Why does Ansible not reinstall nginx on the second run?  What property does this
     demonstrate?

3. **Configuration drift:** After the first playbook run, manually edit `/etc/nginx/nginx.conf`
   on the target host (e.g., change the `worker_processes` value).  Re-run the playbook.
   - Does the playbook detect and correct the drift?  Why or why not?
   - What would you need to add to the playbook to manage the nginx configuration file and
     correct drift?

4. **Reflection (≤ 100 words):** In the pet/cattle metaphor, Ansible helps manage
   *mutable infrastructure* (pets).  What is the key operational risk of this approach even
   with a perfect Ansible playbook?  How do immutable container images address this risk?

---

### Homework 2 — Infrastructure as Code: Terraform

**Learning goal:** Use a declarative IaC tool to provision infrastructure; understand the
plan/apply/state cycle.

*Use the local (file-system) Terraform provider or a free-tier cloud account.  The
`local` provider requires no cloud account and is sufficient for the structural tasks.*

**Tasks:**

1. **Local provider warm-up:** Write a Terraform configuration that uses the
   [`local_file` resource](https://registry.terraform.io/providers/hashicorp/local/latest/docs/resources/file)
   to create three files (`server1.txt`, `server2.txt`, `server3.txt`) each containing
   "Hello from Terraform".
   - Run `terraform init`, `terraform plan`, `terraform apply`.
   - Inspect the `terraform.tfstate` file.  What does it record?  Why is this file
     important?

2. **Plan before apply:** Change the content of `server1.txt` to "Updated by Terraform".
   Run `terraform plan` (without applying yet).
   - What does the plan output tell you?  Which resources will be created, changed,
     or destroyed?
   - Run `terraform apply`.  Verify the file changed.

3. **State and drift:** Outside of Terraform, manually delete `server2.txt`.  Run
   `terraform plan` again.
   - What does Terraform report?  Does it detect the out-of-band deletion?
   - Run `terraform apply`.  What does Terraform do?

4. **Reflection (≤ 100 words):** Compare Ansible and Terraform: both implement IaC, but
   with different primary use cases.  What does Terraform do well that Ansible does not,
   and vice versa?  (Hint: think about *provisioning* resources vs. *configuring* software
   on existing resources.)

---

### Homework 3 — CI/CD Pipeline with GitHub Actions

**Learning goal:** Build a complete Continuous Integration / Continuous Delivery pipeline
as code; understand the stages of a modern software delivery workflow.

**Tasks:**

1. **Simple CI:** Create a public GitHub repository containing a minimal FastAPI
   application (reuse the to-do server from Chapter 2 Homework 2 if you like).  Add a
   `requirements.txt` and a `pytest` test file with at least two tests.

   Write a GitHub Actions workflow (`.github/workflows/ci.yml`) that triggers on every
   push to `main` and:
   - Installs Python dependencies
   - Runs `pytest`
   - Reports pass/fail as a commit status check

2. **Container build stage:** Extend the workflow to build a Docker image after the tests
   pass:
   ```yaml
   - name: Build Docker image
     run: docker build -t todo-app:${{ github.sha }} .
   ```
   Add a `Dockerfile` if you don't have one.  Verify the workflow succeeds end-to-end.

3. **Intentional failure:** Introduce a bug that breaks one test.  Push the change.
   - What does GitHub show on the commit?
   - Does the Docker build step run?  (It should not if you have set the stages up
     correctly with `needs:`.)
   - Fix the bug and push again.

4. **Reflection (≤ 100 words):** The lecture distinguishes *push-based CI/CD* (pipeline
   triggers scripts/kubectl) from *pull-based GitOps* (agent in the cluster watches the
   repo).  For which deployment stage (development, staging, production) is each approach
   more appropriate, and why?

---

### Homework 4 — Service Mesh: Linkerd

**Learning goal:** Observe what a service mesh adds to a microservice deployment without
any application code changes; relate mTLS and load balancing to lecture concepts.

*Requires a running Minikube or kind cluster.*

**Tasks:**

1. **Deploy a multi-service app:**  Deploy the
   [Linkerd demo application](https://linkerd.io/2.12/getting-started/) (`emojivoto`) into
   your cluster:
   ```bash
   curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/emojivoto.yml \
     | kubectl apply -f -
   ```

2. **Install Linkerd and inject the mesh:**  Install the Linkerd CLI and control plane,
   then inject Linkerd's sidecar proxy into the `emojivoto` namespace:
   ```bash
   kubectl get -n emojivoto deploy -o yaml \
     | linkerd inject - \
     | kubectl apply -f -
   ```
   Verify injection: `linkerd -n emojivoto check --proxy`.

3. **Observe the mesh:**  Open the Linkerd dashboard (`linkerd viz dashboard`).
   - Find the `web` → `voting` service call and inspect its success rate, request rate,
     and latency.
   - The `emojivoto` app has a deliberate bug causing some requests to fail.  Can you
     identify which service and endpoint is failing from the dashboard — without looking
     at any application code?

4. **mTLS:**  Run:
   ```bash
   linkerd -n emojivoto edges deployment
   ```
   - What does the `SECURED` column show?
   - What does mTLS provide here that plain TLS between services would not?

5. **Reflection (≤ 100 words):**  The lecture says service meshes solve
   *organisation problems* as well as technical ones.  Based on the Linkerd dashboard,
   give one concrete example of an organisational benefit — something a team owning the
   `voting` service could now see without asking the team owning `web` for help.

---

### Homework 5 — Observability: Prometheus and Grafana

**Learning goal:** Instrument a service; collect and visualise metrics; write an alerting
rule — the full observability loop.

**Tasks:**

1. **Instrument a FastAPI service:**  Add Prometheus metrics to your FastAPI to-do
   server using the `prometheus-fastapi-instrumentator` library:
   ```python
   from prometheus_fastapi_instrumentator import Instrumentator
   Instrumentator().instrument(app).expose(app)
   ```
   Run the server and visit `/metrics`.  Identify which metric tracks the total number
   of HTTP requests and which tracks response latency.

2. **Run Prometheus:**  Write a `prometheus.yml` scrape configuration that tells
   Prometheus to scrape your FastAPI service every 15 s.  Start Prometheus with Docker:
   ```bash
   docker run -p 9090:9090 \
     -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
     prom/prometheus
   ```
   In the Prometheus UI, run the query `http_requests_total` and verify it returns data.

3. **Grafana dashboard:**  Start Grafana (`docker run -p 3000:3000 grafana/grafana`),
   add Prometheus as a data source, and create a dashboard with two panels:
   - Request rate (requests per second): `rate(http_requests_total[1m])`
   - 95th-percentile latency: `histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[1m]))`

   Generate some load (e.g., `for i in $(seq 100); do curl -s localhost:8000/todos; done`)
   and take a screenshot of your dashboard.

4. **Alerting rule:**  Write a Prometheus alerting rule that fires if the to-do server
   has been unavailable (no scrape data received) for more than 30 s.  What Prometheus
   alert state transitions would you expect to see when you stop and restart the server?

5. **Reflection (≤ 100 words):**  The lecture lists *metrics*, *logs*, and *traces* as
   the three pillars of observability.  Your Prometheus setup covers metrics.  For a
   bug where one specific request to `POST /todos` returns a 500 error 0.1% of the time,
   which pillar would you reach for first, and why?

---

### Homework 6 — GitOps with ArgoCD

**Learning goal:** Experience pull-based GitOps deployment; see auto-healing in action;
understand the git-as-single-source-of-truth principle.

*Requires a running Minikube or kind cluster and a GitHub account.*

**Tasks:**

1. **Install ArgoCD:**
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd \
     -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```
   Access the UI via port-forwarding and log in with the initial admin password.

2. **Create a Git repository** containing:
   - A `Deployment` YAML for your FastAPI to-do app (3 replicas, image from Docker Hub or
     your registry)
   - A `Service` YAML exposing it on port 8000

   Create an ArgoCD `Application` that points at this repository.  Set the sync policy
   to *automatic*.

3. **Observe auto-sync:**  Edit the Deployment YAML in Git (e.g., change the replica
   count from 3 to 2).  Watch the ArgoCD UI.
   - How long does it take for ArgoCD to detect the change?
   - What does the cluster look like during synchronisation?

4. **Test auto-healing:**  Manually delete one of the running Pods with `kubectl delete pod`.
   - What does ArgoCD do?
   - Now manually scale the Deployment with `kubectl scale deployment ... --replicas=5`.
     Does ArgoCD revert this?  Why?

5. **Reflection (≤ 100 words):**  The lecture describes GitOps as "no other changes to
   environment allowed, only via repo".  What are the practical implications of this rule
   for a team used to making quick fixes by directly running `kubectl` commands in
   production?  Name one advantage and one potential disadvantage.

---

## Dependency Map

```
Slides: Pet vs. cattle, mutable vs. immutable infrastructure, IaC
    → Quiz 1, 2
    → Homework 1 (Ansible)
    → Homework 2 (Terraform)
    → Homework 1 ↔ Homework 2 reflection (compare the two approaches)

Slides: CI/CD, GitOps, ArgoCD
    → Quiz 7, 8
    → Homework 3 (GitHub Actions CI/CD)
    → Homework 6 (ArgoCD GitOps)
    → Homework 3 and 6 form a natural pipeline: CI builds → GitOps deploys

Slides: Service proxy, service mesh
    → Quiz 6
    → Homework 4 (Linkerd service mesh)

Slides: Observability — metrics, logs, traces
    → Quiz 9
    → Homework 5 (Prometheus + Grafana)

Slides: CNI, container runtime, orchestration scheduling
    → Quiz 4, 5
    → Homework 4 (uses Kubernetes orchestration and CNI)

Slides: Kubernetes operators and CRDs
    → Quiz 10
    → (Background understanding for Homework 6: ArgoCD is itself implemented as a K8s operator)
```

Homework 3 (CI/CD) builds on the FastAPI server from Chapter 2 Homework 2 and the Docker
knowledge from the lab assignments.  Homework 4 (Linkerd) builds on the multi-service
Kubernetes setup from Chapter 3 and the load-balancing concepts from Chapter 4.

---

## Notes for the Instructor

- **Quiz 1** (pet vs. cattle) is often answered correctly but for the wrong reasons.  Follow up:
  "If you use Ansible to configure VMs, are those VMs pets or cattle?"  (Answer: still pets —
  Ansible manages mutable state.  Containers with immutable images are the cattle.)

- **Quiz 8** (GitOps auto-rollback) surprises students who assume manual changes to a running
  cluster are "safe".  Good segue into discussion of configuration drift and the value of
  treating git as ground truth.

- **Homework 1** (Ansible idempotency) works well as a lab exercise with shared VMs.  The
  configuration-drift sub-task (Task 3) is the most educational: students often expect Ansible
  to manage everything, but are surprised that it only manages what you explicitly declare.

- **Homework 4** (Linkerd) is best done in pairs — one runs the dashboard while the other
  generates load.  The deliberate `emojivoto` bug is a good conversation starter about
  observability: "How long would it have taken you to find this bug without the dashboard?"

- **Homework 5** (Prometheus) pairs well with the Chapter 4 availability discussion: students
  can now write an alerting rule for "availability < 99.9% over the last hour" using the
  metrics they are already collecting.
