# Exercise 0 answers

## Task 0 - write the ReplicaSet manifest

See `replica-set.yaml` in this directory.

## Task 1 — describe your replicaset and constituent pods

```bash
kubectl describe rs combo-suggester-rs
kubectl describe pod combo-suggester-rs-<randomsuffix>
```

## Task 2 — update replicaset to have 2 replicas by updating manifest

See `replica-set-2-replicas.yaml` in this directory (you'd just update your `replica-set.yaml` but this directory has both versions for clarity.

## Task 3 — update replicaset with kubectl scale

```bash
kubectl scale rs/combo-suggester-rs --replicas=4
```