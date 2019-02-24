# Lab 3 — Kubernetes Services

## Introduction

> A Kubernetes Service is an abstraction which defines a logical set of Pods and a policy by which to access them - sometimes called a micro-service. 
>
> — [Kubernetes docs](https://kubernetes.io/docs/concepts/services-networking/service/)

When running applications on Kubernetes, you often want to find pods so you can make web requests to them — if you've deployed two microservices (say...`pizza-builder-frontend` and `topping-suggestion-api-service`), you need a way to reliably reach `topping-suggestion-api-service` (otherwise how will people learn that anchovy pineapple is their ideal slice?). Enter Kubernetes [services](https://kubernetes.io/docs/concepts/services-networking/service/). When you create a service, you provide a stable [`ClusterIP`](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)[^0] and DNS name that distributes inbound traffic to a set of pods (this is also known as ([load balancing](https://en.wikipedia.org/wiki/Load_balancing_(computing))). Pods are included in a service by virtue of matching its configured labels. So this service, for example, will forward requests to `topping-suggestion-api-service` to pods with label `app`=`topping-combo-suggestion-api`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: topping-suggestion-api-service
spec:
  ports:
  - targetPort: 80
  selector:
    app: topping-suggestion-api
```

You can expose services in a variety of ways, both within and outside the cluster:

*  `ClusterIP` — service is available at a stable IP inside of the Kube cluster. Access with `curl ClusterIp`.
* `NodePort` — service is available at `ClusterIP` and available on a specific port on each cluster node (so you can `curl any.node.ip.address:nodeport`). 
* `LoadBalancer` — provisions a `LoadBalancer` wherever the cluster is hosted and routes traffic from there to the service. You can `curl load-balancer-url:port` to access it. This makes the service accessible from outside the cluster. Note: if you're running in `minikube` this type of service [may take some work to set up](https://github.com/kubernetes/minikube/issues/384).
* `ExternalName` — makes a DNS name addressable with [Kubernetes service semantics](https://kubernetes.io/docs/concepts/services-networking/service/#externalname). This is quite different than exposing pods as a service, so we won't cover it in this lab

## Prework — Setting up a cluster

This lab assumes you have a running Kubernetes cluster and `kubectl` configured to interact with that cluster. For instructions on doing that, see [lab 1](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/1-kube-clusters).

## Exercise 0 — Creating a service with a `ClusterIP`

In this exercise, we will create a service that's accessible at a `ClusterIP`. 

**Tasks:**

0. Make sure there are no pods running in the `default` namespace and `delete` any running pods (unless you're doing things outside of this tutorial in your cluster, of course).
1. Look over `frontend-pod.yaml` and `utility-pod.yaml` and then add the pods from each  file into the cluster with `kubectl create `(see [lab 2 for more](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/2-kube-pods)).
2. Create a file called `service.yaml` and configure a service (type: `ClusterIP`) that takes in-cluster requests to `frontend` and forwards them to the pod described in `frontend-pod.yaml`. Create the service in the cluster with `kubectl create`.
3. Use `kubectl describe` to find your `service`'s ClusterIP. Next, get inside the running `utility` pod and use `nslookup` to find out which IP requests to `frontend` go to (it should match what showed up in `describe`). 
4. While inside the `utility` pod, `curl` the `frontend` service to  make sure everything's working. If you get an HTML response, things are configured properly.

**Useful docs:** [service docs](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types), [`kubectl describe`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe), [`nslookup`](https://linux.die.net/man/1/nslookup), [lab 2](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/2-kube-pods).

##Exercise 1 — Creating a service with a `NodeIP`

In this exercise, we will create a service that's accessible on a specific port of every node in the cluster.

**Tasks:**

0. Make sure there are no other `frontend` services remaining in the cluster (that is: delete the one from exercise 0 if it's still around).`kubectl delete` as needed.
1. Create a file called `service-nodeport.yaml` that takes requests to any node on port `30789` and forwards them to the pod described in `frontend-pod.yaml`.
2. Get each of your cluster nodes' IP addresses with `kubectl describe` and them paste them somewhere. Get inside the `utility` pod and `curl` each node's IP on port 30789 and verify that you get an HTML response.

**Useful docs:** [service docs](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types), [`kubectl describe`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe).

## Exercise 2 — Creating a service with a LoadBalancer

In this exercise, we will create a service that's accessible outside the cluster using the `LoadBalancer`. Note: if you're running Kubernetes on a cloud provider, this can cost money! Make sure to shut things down when you're done!

**Tasks:**

0. Make sure there are no other `frontend` services remaining in the cluster (that is: delete the one from exercises 0 and 1 if they're still around). `kubectl delete` as needed.
1. Create a file called `service-loadbalancer.yaml` that provisions a load balancer on your cluster's cloud provider and forwards requests to the pod described in `frontend-pod.yaml`. Create the service in the cluster with `kubectl create`.
2. Go to your cloud provider's user interface and find your load balancer.
3. Visit `your-loadbalancer.yourcloudprovider.com` in a browser and verify that an HTML response is present.

**Useful docs:** [service types](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)

## Exercise 3 — Adding pods to a service

In this exercise, we'll add a second pod to the `frontend` service created in exercise 2 — this isn't a normal workflow but will demonstrate how services load balance across member pods.[^1]

**Tasks:**

0. Create a second file (`frontend-pod-2`, perhaps) configuring a pod that will join the `frontend` service. Add the pod to the cluster with `kubectl create`. The pod should have a different name than the one specified `frontend-pod.yaml`.
1. Hit your service using `your-loadbalancer.yourcloudprovider.com` several times and verify that the hostname on the front page changes. 

## Exercise 4 — Clean up

The `LoadBalancer` resource can cost money! Let's make sure we clear everything out of the cluster before going to [lab 4](#todo):

**Tasks:**

0. Delete all pods in the cluster.
1. Delete all services in the cluster.
2. Go to your cloud provider's UI and make sure that you don't have any load balancers provisioned anymore.

**Useful docs:** [`kubectl delete`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#delete)

[^0]: Cluster IPs stay the same for the life of the service.
[^1]: You'd typically control this type of thing with a [`deployment`](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) which we'll learn about in [lab 4}(#todo).