# Lab 4 — Kubernetes `ReplicaSets`

## Introduction

### What's a `ReplicaSet` and why do we have them?


In production software deployments, there's often more than one copy of a given application running. In the case of HyprSk8l Pizza, growing demand for the killer app requires that we always have 3 replicas of our CPU-intensive `topping-suggestion` app running to handle the crushing load (it uses a lot of AI...stuff). These replicas will be part of the `topping-suggestion` Kubernetes service, so traffic will be load-balanced across them. As lab 3 demonstrated, pods belong to the same service aren't necessarily based on the same image, but in the case of the `topping-suggestion` service, we just want three replicas of a `topping-suggestion` pod that runs the app.

As in lab 3, we could create three almost-identical files, `topping-suggestion-pod-[1|2|3].yaml` with labels configured to join a service, and then manually launch each one with `kubectl apply`. But as we know, the `topping-suggestion` app is prone to random failures -- the microservice is prone to random failure, which is one of the reasons we're switching to Kubernetes. So in addition to launching `pizza-topping-picker-pod-[1|2|3]` manually, we'd need to monitor the individual pods to make sure they're up. What a nightmare. Wouldn't it be nice if we could just say "I want three instances of the `topping-suggestion` pod running" and have the cluster handle things for us?  In the words of Homer Simpson, "[can't someone else do it?](https://cdn-images-1.medium.com/max/800/1*P-adWnXHrR_HfC13xC-YPA.gif)" 

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

## Prework

This lab assumes you have a running Kubernetes cluster and `kubectl` configured to interact with that cluster. For instructions on doing that, see [lab 1](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/1-kube-clusters).

## Exercise 0 — Creating a `ReplicaSet`

**Tasks:**

0. Write the manifest for a `ReplicaSet` with three identical pods that serve the `topping-suggestion` application (there's a pre-baked Docker image at `ponderosa/topping-suggestion:1.3` and a working pod spec in the `resources/` directory). Add the `ReplicaSet` to the cluster with `kubectl apply`. 
0. `kubectl describe` can get you more information about your `ReplicaSet`. Use it to figure out the first three events that are associated with the `ReplicaSet`. Next, use `kubectl describe` to find out who the pod is `Controlled By`.
0. Update the ReplicaSet to have two replicas and use `kubectl apply`to update the cluster. Use `kubectl get pods` and `kubectl describe rs` to evaluate the results.
0. Use `kubectl scale` to increase the replica count to 4 and verify the results.

**Useful docs:** [`ReplicaSet` overview](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/), [`ReplicaSet` docs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.13/#replicaset-v1-apps),  [`kubectl scale`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#scale), [`kubectl apply`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply). [`kubectl describe`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe).

## Exercise 1 — Proving a `ReplicaSet` works

Note: skip this if you're running in MiniKube.

**Tasks:**

1. Delete all of the pods in your `ReplicaSet` using `kubectl delete pod`.[^0]
2. Find the node that one of your pods is running on, and run `kubectl drain` to remove all pods from it. Where do the pods go? Once you find the pods, run `kubectl uncordon` to bring the node back into the cluster.

**Useful docs:** [safely drain a node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/#use-kubectl-drain-to-remove-a-node-from-service), [`kubectl drain`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#drain), [`kubectl uncordon`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#uncordon).

## Exercise 2 — Removing a pod from a `ReplicaSet`

**Tasks**:

0. `ReplicaSet` membership is determined by pod labels. Remove a pod from the `ReplicaSet` by using `kubectl edit`. How many pods are now running in the cluster?
0. Change the pod you removed from the `ReplicaSet` to rejoin it using `kubectl edit`. How many pods are now running in the cluster?

**Useful docs:** [`kubectl edit`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#edit). 

## Exercise 3 — Pointing a service at the `ReplicaSet`

Now that we have a resilient set of pods containing our `topping-suggestion` application, it's makes sense to expose them as a service (see [Lab 3](#todo) for more details on that).

**Tasks**:

0. Create a `ClusterIP` service called `topping-suggestion` that serves port 80 traffic to our `ReplicaSet`'s pods (the container is serving traffic on port 9876, as indicated in `resources/topping-suggester-pod.yaml`). You may want to refer to the service definitions in the `labs/3-services/answers` directory.
0. Launch the `utility` pod in `resources/utility-pod`, shell in, and `curl` your new service's `/topping_combo` endpoint.

## Exercise 4 — Deleting a `ReplicaSet`

If you delete a `ReplicaSet`, it will also delete the pods that it manages. By using the `--cascade=false` flag, you can prevent it from doing that.

0. Delete your `ReplicaSet` without deleting its constituent pods.
0. Delete all pods in the cluster.
0. Delete your `topping-suggestion` service.

[^0]: Note that `scale` is an [_imperative_](https://kubernetes.io/docs/concepts/overview/object-management-kubectl/overview/#imperative-commands) object management technique, while `kubectl apply -f my-cool-yaml.yaml` is a [_declarative_](https://kubernetes.io/docs/concepts/overview/object-management-kubectl/declarative-config/) object management technique. It's generally best to stick to one or the other, rather than mixing them.

[^0]: You can't. It's fun to try though!
