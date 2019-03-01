# Exercise 3 answers

## Task 0 — deleting a ReplicaSet without deleting its constituent pods

```bash
kubectl delete rs combo-suggester-rs --cascade=false
```

## Task 1 — deleting pods by  label selector

```bash
kubectl delete po -l app=topping-suggestion
```