# Exercise 3 answers

## Task 0 — creating a service pointing to the ReplicaSet pods

Please see `service.yaml` in this directory for the service definition.

## Task 1 — curl the service you just launched

```bash
kubectl apply -f resources/utility-pod.yaml
kubectl exec -it utility bash
curl topping-suggestion/topping_combo
```
