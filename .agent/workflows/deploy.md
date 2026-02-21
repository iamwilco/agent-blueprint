# Deploy Workflow
**Trigger:** `/deploy`

## Graph
```
[START] → pre_checks → build_image → run_tests
  → {tests_pass?} → push_image → deploy_target → health_check
    → {healthy?} → report_success → [END]
    → rollback → report_failure → [END]
  → abort → report_failure → [END]
```

## Nodes

### 1. pre_checks
- Confirm on correct branch (`main` or `release/*`).
- Confirm no uncommitted changes (`git status --porcelain`).
- Confirm env vars set: `REGISTRY_URL`, `DEPLOY_TARGET`, `IMAGE_TAG`.

### 2. build_image
```bash
export IMAGE_TAG=$(git rev-parse --short HEAD)
docker build -t ${REGISTRY_URL}/app:${IMAGE_TAG} .
```
**Exit:** proceed to `run_tests`.

### 3. run_tests
```bash
docker run --rm ${REGISTRY_URL}/app:${IMAGE_TAG} pytest tests/ -x
```
**Exit:** if pass → `push_image`; if fail → `abort`.

### 4. push_image
```bash
docker push ${REGISTRY_URL}/app:${IMAGE_TAG}
```

### 5. deploy_target
Adapt per platform:
```bash
# AWS ECS
aws ecs update-service --cluster prod --service app --force-new-deployment

# Fly.io
fly deploy --image ${REGISTRY_URL}/app:${IMAGE_TAG}

# Kubernetes
kubectl set image deployment/app app=${REGISTRY_URL}/app:${IMAGE_TAG}
```

### 6. health_check
```bash
# Poll health endpoint for up to 60s
for i in $(seq 1 12); do
  curl -sf https://app.example.com/health && exit 0
  sleep 5
done
exit 1
```
**Exit:** if healthy → `report_success`; if unhealthy → `rollback`.

### 7. rollback
```bash
# Revert to previous image tag
kubectl rollout undo deployment/app
# or: aws ecs update-service --task-definition <previous>
```

### 8. report_success / report_failure
Log outcome to `learning/reflection-log.md`. Include: image tag, deploy duration, health check result.
