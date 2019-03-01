# Exercise 1 answers

## Task 0 — creating a `NodeIP` service

Please see `service-nodeport.yaml` for configuration.

## Task 1 — get node IPs and curl service via NodeIP

```
kubectl get nodes 
kubectl describe node <some-node-identifier> | grep IP
kubectl exec -it utility bash
curl <node_ip>:30789/pizza
```

## Task 2 — curl service via ClusterIP and DNS

```
kubectl describe service frontend-via-nodeport | grep ClusterIP
kubectl exec -it utility bash
# Hit the service using its ClusterIP
curl <ClusterIP>:81/pizza
# Hit the service using dns
curl frontend-via-nodeport:81/pizza
```
