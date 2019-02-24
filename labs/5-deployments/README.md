# Lab 5 — Kubernetes Deployments

## Introduction

Given the profound societal importance of our AI-powered pizza ordering platform, we need to roll it out very carefully. Fortunately, Kubernetes has a first-class way of rolling out new versions of a software application: the [`deployment`]().

> A *Deployment* controller provides declarative updates for [Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/) and [ReplicaSets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/).
>
> You describe a *desired state* in a Deployment object, and the Deployment controller changes the actual state to the desired state at a controlled rate. You can define Deployments to create new ReplicaSets, or to remove existing Deployments and adopt all their resources with new Deployments.
>
> — [Kubernetes docs](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

As with a `ReplicaSet` — one of which is created by a `deployment` under the hood — the `deployment` is _declarative_. You tell Kubernetes what you want to exist in the cluster, and the cluster makes it happen.

Deployments give you lots of switches and knobs to choose from when you're configuring them — you can see an summary [here](https://kubernetes.io/docs/concepts/workloads/controllers/deployment) and an exhaustive list in the [`deployment` docs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.13/#deploymentspec-v1-apps) (don't forget to look at the [`deploymentStrategy`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.13/#deploymentspec-v1-apps)) docs as well. We're mostly going to be concerned with the deployment [_strategy_](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy) (`RollingUpdate` or `Recreate`). Per the [Kubernetes docs](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment), a deployment manifest looks like this:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80

```



## Prework

* This lab assumes you have a running Kubernetes cluster and `kubectl` configured to interact with that cluster. For instructions on doing that, see [lab 1](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/1-kube-clusters).

## Exercise 0 — Creating a deployment

HyperscalePizza has moved their workloads from the datacenter onto Kubernetes and the increased pace of deployment has made revenue go up and to the right, 🍕↗. Unfortunately, they're managing they're managing rollout of new application versions by deleting the previous application's `ReplicaSet`, updating the container image specified in the `replicaSet` manifest, then running `kubectl apply -f replica_set.yaml`. You've heard that `deployment`s might help, so you decide to make one as a proof of concept.

**Tasks:** 

0. Create a `deployment` manifest that specifies 2 replicas of the `ponderosa/topping-combo-suggester-slow-startup:0.2` image and launch it into the cluster with `kubectl apply -f deployment.yaml`. Check that your pods are running with `kubectl get pods`.
1. Create a `service` that sends traffic to the pods launched by the deployment (you can probably use the service manifest you did in [lab 3](#todo))
2. Launch a service containing the `health-checker-app` by running `./run-health-checker.sh your-service-name` in this directory. The health checker provides diagnostic info on the `toping-combo-suggetser` service running at `your-service-name`. TODO: clean this up
3. In one window, pull up the `pizza-health-checker` UI. In another window, update `deployment.yaml` to specify that there should be three replicas, then launch it into the cluster with `kubectl apply -f deployment.yaml` and check that you have three pods running. Watch the UI and look for 500s from the `topping-combo-sugester` service. What do you see? 

**Useful docs:** [`deployments`](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), [`service` docs](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)

## Exercise 1 — Adding a readinessProbe

As you might have noticed, our service started delivering traffic to our new replica before it was ready (note that it's called `topping-combo-suggester-slow-startup`). Hungry pizza orderers are seeing errors as a result! We can fix this by setting a `readinessProbe` on our pod. A `service` will only load balance to matching pods if their `readinessProbe` shows them as ready.

**Tasks**: 

0. Add a `readinessProbe` to the `topping-combo-suggester-slow-startup` pod that hits the `/health-check` endpoint. Pull up your `pizza-health-checker` UI and then, in a separate window, update your `deployment` with `kubectl apply`. What do you see?

**Useful docs:** [liveness and readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/), [services](https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service)

## Exercise 2 — Toggling deployment strategy

The time has come to upgrade `topping-combo-suggester-slow-startup` to the hot new release, `topping-combo-suggester:0.2`. Due to their extremely complex machine learning algorithms, code running in `topping-combo-suggester-slow-startup` cannot be run concurrently with `topping-combo-suggester`, which means we need to kill all `topping-combo-suggester-slow-startup` pods before firing up the new `topping-combo-suggester:0.2` pods. 

0. Configure the deployment's `strategy` field to kill the old version's pods entirely before starting up the new ones.

**Useful docs**: [deployment strategy](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy).

## Followup exercises:

* Undo your latest rollout using [`kubectl rollout undo`](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-to-a-previous-revision).
* Rollout a new deployment with four replicas of `topping-combo-suggester:0.3`, making sure that there are always at least 2 pods available using the [`maxUnavailable` field](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#max-unavailable). 
* Update your manifest to deploy four replicas of `topping-comb-suggester-slow-startup:0.2` with `maxUnavailable` set to 25%. After ten seconds, [pause the deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#pausing-and-resuming-a-deployment). View the status with `kubectl rollout status`. When you're ready, resume the deployment.



Followup Exercises:

- deployment proportions