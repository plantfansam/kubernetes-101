# Exercise 3 Answers

## Task 0 — create files inside of running pod

```
kubectl exec -it hs-pizza-frontend bash
mkdir /my-cool-directory
touch /my-cool-directory/my-cool-text-file.txt
touch /my-cool-comma-separated-value-file.csv
exit
```

## Task 1 — list files inside of running pod

```
kubectl exec hs-pizza-frontend ls /my-cool-directory
```

## Task 2 — delete and recreate pod

```
kubectl delete hs-pizza-frontend
kubectl apply -f pod.yaml
kubectl exec -it hs-pizza-frontend bash
ls / | grep my-cool-directory
# The directory is gone because deleting a pod disposes of the pod's container(s).
# When you created a new pod, it spun up a fresh container based on its underlying image.
```

