# Lab 6 — Namespaces

## Introduction

After raising a series C of $100 million, HyprSkale Pizza is investing heavily in the the stability of the app, along with an in-house brick oven pizzeria. Gone are the days of testing in production. The VP of Engineering, Kara Marinara, has told the DevOps team to create a `staging` environment where engineers can test out new code before deploying to production. We'll use `namespaces` to do it.

### What's a namespace?

> Kubernetes supports multiple virtual clusters backed by the same physical cluster. These virtual clusters are called namespaces.
>
> — [Kubernetes docs](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

Namespaces are fairly intuitive — things inside of one namespace only see things inside of their namespace by default. It's possible to reach from one namespace to another, but somewhat of a pain. Consider the following: you have a `topping-combo-suggestion-service` service in your `production` namespace and a `topping-combo-suggestion-service` in your `staging` namespace. There's one `utility` pod hanging around each namespace. If you `curl topping-combo-suggestion-service` from the `production` `utility` pod, you will get the `topping-combo-suggestion-service` registered in the `production` namespace. Likewise, if you `curl topping-combo-suggestion-service` from the `staging` `utility` pod, you will get that namespace's `topping-combo-suggestion-service` service. If you wanted to reach from `staging` to the service in `production`, you'd need to hit `topping-combo-suggestion-service.production.svc.cluster.local` (note the `.production` portion).

## Prework

- This lab assumes you have a running Kubernetes cluster and `kubectl` configured to interact with that cluster. For instructions on doing that, see [lab 1](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/1-kube-clusters)

## Exercise 0 — Listing and creating namespaces

**Tasks**: 

0. List all of the namespaces in your cluster using `kubectl get`
1. Get the namespace resource quota for the `kube-system` namespace using `kubectl describe`
2. Create a `staging` namespace in your cluster using `kubectl create`

**Useful docs**: [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

## Exercise 1 — Making requests inside of namespaces

0. Launch the pod defined in `utility-pod` into the `staging` namespace.
1. Use `kubectl get pods` to get _only_ those pods in the `staging` namespace.
2. Delete `utility-pod`.

**Useful docs**: [setting the namespace for a request](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#setting-the-namespace-for-a-request), [`kubectl describe`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe).

## Followup exercises

* Read about `contexts` in the [docs](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/) and create a "staging" and "production" context.
* List the pods that are running in the `kube-system` namespace and look up what they're doing.
* Use `kubectl api-resources` (docs are [here](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#api-resources)) to figure out which resources in the cluster do and don't belong to a namespace

