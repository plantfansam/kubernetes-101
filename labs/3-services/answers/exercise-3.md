# Exercise 3 Answers

## Task 0 — examine endpoints

```bash
kubectl describe service frontend-via-loadbalancer-service
```

## Task 1 — update labels so that pod defined in frontend-pod-3.yaml joins the service

See `frontend-pod-3.yaml` in this directory.

## Task 2 - reexamine endpoints

```bash
kubectl describe service frontend-via-loadbalancer-service
```

## Task 3 — hit service's /pizza endpoint

```bash
# if you're not using a LoadBalancer service, shell into the utility pod; otherwise just use your LoadBalancer's url
kubectl exec -it utility bash
curl <your-service-name>:80/pizza
```