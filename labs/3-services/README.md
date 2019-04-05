# Lab 3 — Kubernetes Services

## Introduction

> A Kubernetes Service is an abstraction which defines a logical set of Pods and a policy by which to access them - sometimes called a micro-service. 
>
> — [Kubernetes docs](https://kubernetes.io/docs/concepts/services-networking/service/)

When running applications on Kubernetes, HyprSk8l Pizza will need to find pods in order to route network requests to them — remember, we're not going to use `kubectl port-forward` in production. This is particularly relevant because HyprSk8l Pizza recently made the leap to [microservices](https://microservices.io/); not only do end users need to access the `hs-pizza-frontend` from the internet, `hs-pizza-frontend` needs  to talk to the `topping-suggestion-service` in order to deliver value to customers (otherwise how will people learn that anchovy pineapple is their ideal slice?).

Enter Kubernetes [services](https://kubernetes.io/docs/concepts/services-networking/service/). When you create a Kubernetes service, Kubernetes provide a stable [`ClusterIP`](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)[^0] and DNS name that distributes traffic to a defined set of pods (this is also known as ([load balancing](https://en.wikipedia.org/wiki/Load_balancing_(computing))). **Pods are included in a service by virtue of matching its configured labels.** So the following service, for example, would forward in-cluster requests to `topping-suggestion-service` to pods with the label `app`=`topping-suggestion`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: topping-suggestion-service
spec:
  ports:
  - targetPort: 80
  selector:
    app: topping-suggestion
```

You can expose services in a variety of ways, both within and outside the cluster:

*  `ClusterIP` — service is available at a stable IP inside of the Kube cluster. Access with `curl ClusterIp`.
*  `NodePort` — service is available at `ClusterIP` and available on a specific port on each cluster node (so you can `curl any.node.ip.address:nodeport`). 
*  `LoadBalancer` — provisions a `LoadBalancer` wherever the cluster is hosted and routes traffic from there to the service. You can `curl load-balancer-url:port` to access it. This makes the service accessible from outside the cluster. Note: if you're running in `minikube` this type of service [_may_ take some work to set up](https://github.com/kubernetes/minikube/issues/384).
*  `ExternalName` — makes a DNS name addressable with [Kubernetes service semantics](https://kubernetes.io/docs/concepts/services-networking/service/#externalname). This is quite different than exposing pods as a service, so we won't cover it in this lab.

## Prework — Setting up a cluster

This lab assumes you have a running Kubernetes cluster and `kubectl` configured to interact with that cluster. For instructions on doing that, see [lab 1](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/1-kube-clusters).

## Exercise 0 — Creating a service with a `ClusterIP`

Let's get HyprSk8l's `frontend-python` service up and running and then we can add in the topping suggestion microservice interactions. The simplest way to expose a service is via `ClusterIP` — in a `ClusterIP` service, Kubernetes DNS will also resolve in-cluster calls to `the-service-name` to that `ClusterIP`. 

**Prework:**

0. Make sure there are no pods running in the `default` namespace and `delete` any running pods (unless you're doing things outside of this tutorial in your cluster, of course).
1. Look over `frontend-pod.yaml`, `frontend-pod-2.yaml` and `utility-pod.yaml` in the `resources` directory and then add the pods from each  file into the cluster with `kubectl apply -f resources/frontend-pod.yaml -f resources/frontend-pod-2.yaml -f resources/utility-pod.yaml` (your path may vary based on where you run these commands from; see [lab 2 for more details on creating Kubernetes pods](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/2-kube-pods)).

**Tasks:**

0. Create a manifest (`service-clusterip.yaml`) that specifies a service with the name `frontend-via-clusterip`. The service should forward requests on port 81 to port 5000 in any pod with the label `app=hs-pizza-frontend`. The service should be of `type: ClusterIP`. Create the service in the cluster with `kubectl apply -f service-clusterip.yaml`.
0. Use `kubectl describe` to find your `service`'s ClusterIP.
0. Shell into the running `utility` pod using `kubectl exec` then and use `nslookup` to find out the IP that requests to `frontend-via-clusterip` go to (it should match what showed up when you ran `describe` on the service). 
0. While inside the `utility` pod, `curl` the `/pizza` endpoint of `frontend-via-clusterip` service on (make sure you've got the port specified) to make sure everything's working. If you get an HTML response, things are configured properly.
0. Delete your service when you're done using `kubectl delete`.

**Useful docs:** [service docs](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types), [`kubectl describe`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe), [`nslookup`](https://linux.die.net/man/1/nslookup), [lab 2](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/2-kube-pods).

## Exercise 1 — Creating a service with a `NodePort`

In this exercise, we will create a service that's accessible on a specific port of every node in the cluster.

**Tasks:**

0. Create a manifest (`service-nodeport.yaml`) that specifies a service with the name `frontend-via-nodeport`. The service should forward requests to any node on port `30789` and forward them to any pod with the label `app=hs-pizza-frontend`. Launch the service into your cluster with `kubectl apply`.
0. Get one of your cluster nodes' IP addresses with `kubectl describe` and copy it. Get inside the `utility` pod and `curl` that node on port 30789, hitting the `/pizza` endpoint. 
0. Get the `frontend-via-nodeport`'s ClusterIP using `kubectl describe` and hit the `/pizza` endpoint using `ClusterIP` and using DNS.
0. Delete your service.

**Useful docs:** [service docs](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types), [`kubectl describe`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe).

## Exercise 2 — Creating a service with a LoadBalancer

In this exercise, we will create a service that's accessible outside the cluster using the `LoadBalancer`. Note: if you're running Kubernetes on a cloud provider, this costs money! Make sure to shut things down when you're done!

**Tasks:**

0. Create a manifest (`service-loadbalancer.yaml`) that specifies a service with the name `frontend-via-loadbalancer`. The service should forward requests on port 80 to port 5000 on a pod with the label `app=hs-pizza-frontend`. Launch the service into your cluster with `kubectl apply`.
0. Go to your cloud provider's user interface and find your load balancer.
0. Visit `your-loadbalancer.yourcloudprovider.com/pizza` in a browser and verify that a response is present.

**Useful docs:** [service types](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)

## Exercise 3 — Adding pods to a service

In this exercise, we'll add a third pod to the `frontend` service created in exercise 2 — this isn't a normal workflow but will demonstrate how services load balance across member pods.[^1]

**Tasks:**

0. Check out the `Endpoints` associated with your `frontend-via-loadbalancer service` by using `kubectl describe`; note how many there are.
0. Update the labels on `resources/frontend-pod-3.yaml` so that it will join your `frontend-via-loadbalancer` service. Add the pod to the cluster with `kubectl apply -f`. Note that this pod intentially contains a different image than others in itopping suggestion service, which is _extremly_ not recommended; we're only doing it for demonstration purposes.
0. Check out the `Endpoints` associated with your service again; you should see one more.
0. Hit your service's `/pizza` endpoint repeatedly until it's obvious that the new pod has joined the service.

## Exercise 4 — Clean up

The `LoadBalancer` resource can cost money! Let's make sure we clear everything out of the cluster before going to [lab 4](#todo):

**Tasks:**

0. Delete all pods in the cluster (`kubectl delete --all pods`).
1. Delete all services you created in this lab.
2. Go to your cloud provider's UI and make sure that you don't have any load balancers provisioned anymore.

**Useful docs:** [`kubectl delete`](https://kubernekkktes.io/docs/reference/generated/kubectl/kubectl-commands#delete)

[^0]: Cluster IPs stay the same for the life of the service.
[^1]: You'd typically control this type of thing with a [`deployment`](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) which we'll learn about in [lab 4}(#todo).