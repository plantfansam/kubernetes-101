# Exercise 5 answers

## Task 0 — annotating a node with best_topping

```bash
kubectl annotate node minikube best_topping=pineapple
kubectl describe node minikube | grep -i pineapple
```

## Task 1 — specifying annotation in pod manifest

```bash
kubectl delete pod hs-pizza-frontend
kubectl apply -f pod-with-annotations.yaml
kubectl describe pod hs-piza-frontend | less
```



