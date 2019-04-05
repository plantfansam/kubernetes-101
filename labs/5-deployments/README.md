# Lab 5 — Kubernetes Deployments

## Introduction

We've moved HyprSk8l Pizza's workloads from the datacenter onto Kubernetes and the increased pace of deployment has made revenue go up and to the right 🍕📈! Unfortunately, they're managing we're managing rollout of new application versions by deleting the previous application's `ReplicaSet`, updating the container image specified in the `ReplicaSet` manifest, then running `kubectl apply -f replica_set.yaml`. The new `ReplicaSet` pods join the specified services by virtue of having the appropriate labels, but there's downtime between deleting the old ReplicaSet and creating a new one. Given the profound societal importance of our AI-powered pizza ordering platform, we need to roll out new versions carefully and without outages. Fortunately, Kubernetes has a first-class way of rolling out new versions of a software application: the [`deployment`](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/). A deployment manages ReplicaSets and their constituent pods.

> A *Deployment* controller provides declarative updates for [Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/) and [ReplicaSets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/).
>
> You describe a *desired state* in a Deployment object, and the Deployment controller changes the actual state to the desired state at a controlled rate. You can define Deployments to create new ReplicaSets, or to remove existing Deployments and adopt all their resources with new Deployments.
>
> — [Kubernetes docs](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

As with a `ReplicaSet` — one of which is created by a `deployment` under the hood — the `deployment` is _declarative_. You tell Kubernetes what you want to exist in the cluster, and the cluster makes it happen.

Deployments give you lots of switches and knobs to choose from when you're configuring them — you can see an summary [here](https://kubernetes.io/docs/concepts/workloads/controllers/deployment) and an exhaustive list in the [`deployment` docs](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.13/#deploymentspec-v1-apps) (don't forget to look at the [`deploymentStrategy`](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.13/#deploymentspec-v1-apps); there's two options: `RollingUpdate` and `Recreate`) docs as well. Per the [Kubernetes docs](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment), a deployment manifest looks like this:

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
  strategy:
    type: RollingUpdate
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

**Tasks**:

0. HyprSk8l Pizza's crack SRE (site reliability engineering) squad has written Kubernetes config for a cool new service health dashboard. Launch the dashboard by running `kubectl apply -f resources/health-checker-deployment.yaml -f health-checker-service.yaml`.
0. Get the pod's name with `kubectl get pods` and start forwarding local traffic to the health checker with `kubectl port-forward <podname> 5000:5000`. Visit http://localhost:5000 to verify that the dashboard is up. Note the health status of the topping-suggestion service and frontend service.  
0. Launch the utility pod specified in `resources/utility-pod.yaml`.

## Exercise 0 — Creating a deployment

In this exercise, we'll create a deployment and a service that sends traffic to its pods.

**Tasks:** 

0. Create a `deployment` manifest in `topping-suggestion-deployment.yaml` that specifies 2 replicas of a pod containing the `ponderosa/topping-suggestion:1.3` image (see `resources/topping-suggester-pod.yaml` for a working pod spec). Launch it into the cluster with `kubectl apply -f deployment.yaml` and check that your pods are running with `kubectl get pods`.
0. Create a service called `topping-suggestion` that sends traffic on port 80 to the pods specified in the `deployment` you just created.[^0]).
0. Visit your health checker dashboard to verify that the `topping-suggestion` service is now up.[^0]

## Exercise 1 — Updating a deployment

0. Update your `topping-suggestion` deployment to point to the `topping-suggestion-slow-startup:1.3` image, which is the exact same thing as the `topping-suggestion` image, except it's configure to start the application after 90 seconds. Update your deployment with `kubectl apply`.
0. Run `watch kubectl get pods` to see what's happening in the cluster. Meanwhile, pull up your `pizza-health-checker` UI and monitor the health of your deployment.
0. Pull up the `pizza-health-checker` UI and refresh it — what happened to the health of the `topping-suggestion` service? 

**Useful docs:** [`deployments`](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), [`service` docs](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)

## Exercise 1 — Adding a readinessProbe

As you might have noticed, our service started delivering traffic to our new replica before it was ready. Hungry pizza orderers might see errors as a result! We can fix this by setting a `readinessProbe` on our pod. A `service` will only load balance to matching pods if their `readinessProbe` shows them as ready.

**Tasks**: 

0. The `topping-suggestion-slow-startup` container has a `/health-check` endpoint on port 9876 that can be used to figure out if the container is ready to serve traffic. Add a `readinessProbe` to the `topping-suggestion-slow-startup` pod that hits it and update your deployment with `kubectl apply`.
0. Run `watch kubectl get pods` to see what's happening in the cluster, taking note of the `Ready` column. Meanwhile, pull up your `pizza-health-checker` UI and monitor the health of your deployment.

**Useful docs:** [liveness and readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/), [services](https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service)

## Exercise 2 — Toggling deployment strategy

Dissatisfied with all these new slow startup problems, the team has decided to roll back the deployment to `topping-suggestion:1.3`. Due to the extremely complex machine learning algorithms, code running in `topping-suggestion-slow-startup` cannot be run concurrently with `topping-suggestion`, which means we need to kill all `topping-suggestion-slow-startup` pods before firing up the new `topping-suggestion:1.3` pods. 

0. Configure the deployment's `strategy` to use the `Recreate` strategy. Apply your modified deployment definition to the cluster with `kubectl apply`.
0. Run `watch kubectl get pods` to see what's happening in the cluster, taking note of the `Ready` column. Meanwhile, pull up your health cehcker UI and monitor the health of your deployment.

**Useful docs**: [deployment strategy](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy).

## Followup exercises:

* Undo your latest rollout using [`kubectl rollout undo`](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-to-a-previous-revision).
* Rollout a new deployment with four replicas of `topping-suggestion:0.3`, making sure that there are always at least 2 pods available using the [`maxUnavailable` field](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#max-unavailable). 
* Update your manifest to deploy four replicas of `topping-comb-suggester-slow-startup:1.3` with `maxUnavailable` set to 25%. After ten seconds, [pause the deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#pausing-and-resuming-a-deployment). View the status with `kubectl rollout status`. When you're ready, resume the deployment.


[^0]: If you've already completed Lab 4, you can make use of the `service.yaml` manifest you wrote; if not, check out [Lab 3](#todo).
[^0]: Check out `intellipod/app.py` to understand what the health checker is doing. It's not complicated: just hitting the `/health-check` endpoint of each service.