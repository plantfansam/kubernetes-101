# Lab 4 — Kubernetes `ReplicaSets`

## Introduction

### What's a `ReplicaSet` and why do we have them?

> A ReplicaSet’s purpose is to maintain a stable set of replica Pods running at any given time. As such, it is often used to guarantee the availability of a specified number of identical Pods.
>
> — [Kube docs](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)

In large software deployments, there's often more than one copy of a given application running. In the case of our pizza app, growing demand for our killer app may require that we have 3 replicas of our CPU-intensive `topping-combo-suggester` app to handle the crushing load (we'd load balance across the three replicas with a service, which we cover in [lab 3](#todo)). Each of these replicas would be a copy of the same `topping-combo-suggester` pod. One way to handle creating the replicas is to creating three almost-identical files, `topping-combo-suggester-pod-[1|2|3].yaml`, and then manually launch each one with `kubectl create`. As we know, the `topping-combo-suggester` app is prone to random failures, and pods go out of commission every 4-5 minutes. So in addition to launching `pizza-topping-picker-pod-[1|2|3]` manually, we'd need to monitor the individual pods to make sure they're up. What a nightmare. Wouldn't it be nice if we could just say "I want three instances of the `topping-combo-suggester` pod running" and have the cluster handle things for us?  In the words of Homer Simpson, "[can't someone else do it?](https://cdn-images-1.medium.com/max/800/1*P-adWnXHrR_HfC13xC-YPA.gif)" 

Enter the `ReplicaSet`. A `ReplicaSet` keeps a given number of pods running in the cluster at all times. The manifest for a `ReplicaSet` looks about like this:

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

The `spec` refers to the specification for the `ReplicaSet`. The `template` key is a `pod` template that's replicated   

## Prework

This lab assumes you have a running Kubernetes cluster and `kubectl` configured to interact with that cluster. For instructions on doing that, see [lab 1](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/1-kube-clusters).

## Exercise 0 — Creating a `ReplicaSet`

**Tasks:**

0. Write the manifest for a `ReplicaSet` with three identical pods that serve the `topping-combo-suggester` application (there's a pre-baked Docker image at `ponderosa/topping-combo-suggester`. Add the `ReplicaSet` to the cluster with `kubectl create --save-config`. 
1. `kubectl describe` can get you more information about your `ReplicaSet`. Use it to figure out the first three events that are associated with the `ReplicaSet`. Next, use `kubectl describe` to find out who the pod is `Controlled By`.
2. Update the ReplicaSet to have two replicas and use `kubectl apply`to update the cluster.
3. Use `kubectl scale` to increase the replica count to 4.
4. Use `kubectl apply` to decrease the replica count to 1.

**Useful docs:** [`ReplicaSet` overview](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/), [`ReplicaSet` docs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.13/#replicaset-v1-apps),  [`kubectl scale`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#scale), [`kubectl apply`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply). [`kubectl describe`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe).

## Exercise 1 — Proving a `ReplicaSet` works

**Tasks:**

1. Delete all of the pods in your `ReplicaSet` using `kubectl delete pod`.[^0]
2. Find the node that one of your pods is running on, and run `kubectl drain` to remove all pods from it. Where do the pods go? Once you find the pods, run `kubectl uncordon` to bring the node back into the cluster.

**Useful docs:** [safely drain a node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/#use-kubectl-drain-to-remove-a-node-from-service), [`kubectl drain`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#drain), [`kubectl uncordon`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#uncordon).

## Exercise 2 — Removing a pod from a `ReplicaSet`

**Tasks**:

0. `ReplicaSet` membership is determined by pod labels. Remove a pod from the `ReplicaSet` by using `kubectl edit`. How many pods are now running in the cluster?
1. Change the pod you removed from the `ReplicaSet` to rejoin it using `kubectl edit`. How many pods are now running in the cluster?

**Useful docs:** [`kubectl edit`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#edit), 

## Exercise 3 — Deleting a `ReplicaSet`

If you delete a `ReplicaSet`, it will also delete the pods that it manages. By using the `--cascade=false` flag, you can prevent it from doing that.

0. Delete your `ReplicaSet` without deleting its constituent pods.
1. Delete all pods in the cluster.

[^0]: You can't. It's fun to try though!