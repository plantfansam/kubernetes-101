# Exercise 4 answers

## Task 0 — labelling pods

```bash
kubectl label pod utility best_topping=broccoli
kubectl label pod hs-pizza-frontend best_topping=artichokes
```

## Task 1 — showing pods with labels

```bash
kubectl get pods --show-labels
kubectl delete --all pods
```

## Task 2 — update pod manifest to specify label

See `utility-pod.yaml` and `pod.yaml` in this directory.

## Task 3 — retrieve pods that match label best_topping == broccoli

```bash
kubectl get pods --selector best_topping=broccoli
```

## Task 4 — retrieve any pod that has best_topping label

```bash
kubectl get pods --selector best_topping
```





0.  Label one pod with `best_topping=your-favorite-pizza-topping-goes-here` and the other pod with `best_topping=broccoli`. 
1. Get the labels for all of your pods with `kubectl get pods --show-labels`. After verifying that the labels are attached with `kubectl get pods --show-labels`, delete all pods.
2. Update your `.yaml` pod definitions to specify the appropriate `besttopping` label and redeploy the pods. Verify that it worked with `kubectl get pod --show-labels`.
3. Retrieve all pods that have the `best_topping=broccoli` label using `kubectl get`'s `--selector` option.
4. Retrieve all pods that have _any_ value for the `best_pasta_shape` label using `kubectl get`'s `--selector` option.