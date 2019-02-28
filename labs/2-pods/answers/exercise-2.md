# Exercise 2 Answers

## Task 0 -- edit your pod

```
kubectl edit pod hs-pizza-frontend
# edit the "- image:" yaml key to something else
#spec:
#  containers:
#  - image: ponderosa/blahhhh:1.0
```

## Task 1 -- delete your pod

```
kubectl delete pod hs-pizza-frontend
```

## Task 2 -- recreate your pod

```
kubectl create -f pod.yaml
kubectl port-forward hs-pizza-frontend 1234:5000
```

