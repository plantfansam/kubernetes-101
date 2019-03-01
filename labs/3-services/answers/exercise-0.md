# Exercise 0 answers

## Task 0 — create service manifest

Please see `service-clusterip.yaml` for the configuration.

## Task 1 — get service ClusterIP

```bash
kubectl describe svc frontend-via-clusterip | grep IP
```

## Task 2 — use nslookup to find ClusterIP

```bash
kubectl exec -it utility bash
nslookup frontend-via-clusterip
# this should match the IP you found in task 1
```

## Task 3 — curl the /pizza endpoint of the frontend-via-clusterip service

```bash
curl frontend-via-clusterip:81/pizza
```

## Task 4 — delete your service

```bash
kubectl delete svc frontend-via-clusterip
```