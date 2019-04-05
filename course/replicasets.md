# Kubernetes `ReplicaSets`

### What's a `ReplicaSet` and why do we have them?


In production software deployments, there's often more than one copy of a given application running. In the case of HyprSk8l Pizza, growing demand for the killer app requires that we always have 2 replicas of our FE APP and 3 replicas of our CPU-intensive TS APP running to handle the crushing load (it uses a lot of AI...stuff). These replicas will be part of the topping suggestion service, so traffic will be load-balanced across them. In Kubernetes-speak, we want three replicas of a `topping-suggestion` pod that runs the app.

As we did with the frontend service in the previous section, we could create multiple, almost-identical files, `topping-suggestion-pod-[1|2|3].yaml` with their labels configured to join a service, and then manually launch each one with `kubectl apply`. But as we know, the `topping-suggestion` app is prone to random (which, by the way, is one of the reasons we're switching to Kubernetes). So in addition to launching `topping-suggestion-pod-[1|2|3]` manually, we'd need to monitor the individual pods to make sure they're up. What a nightmare. Wouldn't it be nice if we could just say "I want three instances of the `topping-suggestion` pod running" and have the cluster handle things for us?  In the words of Homer Simpson, "[can't someone else do it?](https://cdn-images-1.medium.com/max/800/1*P-adWnXHrR_HfC13xC-YPA.gif)."

Enter the `ReplicaSet`. 

> A ReplicaSet’s purpose is to maintain a stable set of replica Pods running at any given time. As such, it is often used to guarantee the availability of a specified number of identical Pods.
>
> — [Kube docs](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)

A `ReplicaSet` keeps a given number of pods running in the cluster at all times. The manifest for a `ReplicaSet` looks about like this:

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: combo-suggester-rs
  labels:
    app: my-cool-app
spec:
  replicas: 100
  selector:
    matchLabels:
      app: my-cool-app
  template:
    metadata:
      labels:
        app: my-cool-app
    spec:
      containers:
      - name: my-cool-app-pod
        image: the-docker-image
```

The `spec` refers to the specification for the `ReplicaSet`. The `template` key is a `pod` template that's replicated according the the count set in the `replicas` key. Membership in a `ReplicaSet` is determined by the labels. The `ReplicaSet` has a `matchLabels` field; any visible pods in the cluster that match those labels become managed by the `ReplicaSet`. If the `ReplicaSet` is created in the cluster, it will create as many pods as is necessary to reach its replica count.

### Creating a `ReplicaSet` for the FE pods

Let's start by clearing out the pods from our cluster with `kubectl delete --all pods`. Let's also delete the frontend service with `kubectl delete service frontend`. Now, let's make a `ReplicaSet` that ensures we always have two frontend pods running at all times. We can do this with the following YAML:

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend-rs
  labels:
    app: hs-pizza-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: hs-pizza-frontend
  template:
    metadata:
      labels:
        app: hs-pizza-frontend
    spec:
      containers:
        - name: frontend-container
          image: ponderosa/hs-pizza-frontend-service:0.1
          ports:
            - containerPort: 1234
```

Paste this YAML into a new file called `k8s/frontend-replicaset.yaml`. Apply it to the cluster with `kubectl apply -f k8s/frontend-replicaset.yaml`. Check out the replicaset with `kubectl get rs` and see the pods that it's created with `kubectl get pod`.

Try deleting one of the pods with `kubectl delete pod frontend-rs-abcds` and see what happens!

Let's update the `ReplicaSet` to have three replicas and apply the changes to the cluster:

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend-rs
  labels:
    app: hs-pizza-frontend
spec:
  replicas: 3
...
```

What happens?

### Removing a pod from the `ReplicaSet`

`ReplicaSet` membership is determined by pod labels. Let's remove a pod from the `ReplicaSet` by using `kubectl edit`. Check out how many pods are running in the cluster now using `kubectl get pods`. Now, change the pod you removed from the `ReplicaSet` to rejoin it using `kubectl edit` again. How many pods are now running in the cluster?

### Pointing a service at the `ReplicaSet` pods

Now, we've got 3 pods running. Let's re-create the frontend service — you should still have the manifest in `k8s/frontend-service.yaml`, but you can also use `resources/frontend-service.yaml`. Check the endpoints registered as part of the frontend service with `kubectl get endpoints`.

### Deleting a `ReplicaSet`

If you delete a `ReplicaSet`, it will also delete the pods that it manages. By using the `--cascade=false` flag, we can prevent it from doing that. Let's first delete the replicaset we created with `kubectl delete replicaset frontend-rs --cascade=false`. Now, we can delete all of its pods by running `kubectl delete pods -l app=hs-pizza-frontend`. 

## Exercise: creating a `ReplicaSet` for the topping suggestion pod

Just like we want our frontend pods managed by a `ReplicaSet`, we also want our topping suggestion pods managed by a `ReplicaSet`. For this exercise, create a `ReplicaSet` called `topping-suggestion-rs` that expects 3 replicas of the pod specified in `resources/hs-pizza-topping-suggestion-service-pod.yaml`. Launch the `ReplicaSet` into the cluster using `kubectl apply`.