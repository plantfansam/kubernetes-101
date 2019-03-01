# Exercise 2 answers

## Task 0 — remove pod from replicaset

```bash
kubectl get pods -l app=topping-suggestion
kubectl edit pod <pod-name-from-previous-command>
# update label in dialog
# labels:
#   app: watokcool  
```

## Task 1 — add pod back to replicaset

```bash
kubectl edit pod <pod-name-you-just-edited>
# update label in dialog
# labels:
#   app: topping-suggestion
```

`kubectl get pods` shows that one of the pods from the `ReplicaSet` is being terminated because the `ReplicaSet` manages the cluster to only have the specified number of replicas.