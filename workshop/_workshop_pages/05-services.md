---
layout: workshop-page
title: "Kubernetes Services"
---

> A Kubernetes Service is an abstraction which defines a logical set of Pods and a policy by which to access them - sometimes called a micro-service. 
>
> — [Kubernetes docs](https://kubernetes.io/docs/concepts/services-networking/service/)

When running applications on Kubernetes, HyprSk8l Pizza will need to find pods in order to route network requests to them — remember, we're not going to use `kubectl port-forward` in production. This is particularly relevant because HyprSk8l Pizza recently made the leap to [microservices](https://microservices.io/); not only do end users need to access the frontend service from the internet, the frontend service needs to talk to the topping suggestion service in order to deliver value to customers (otherwise how will people learn that anchovy pineapple is their ideal slice?).

Enter Kubernetes [services](https://kubernetes.io/docs/concepts/services-networking/service/). When you create a Kubernetes service, Kubernetes provide a stable [`ClusterIP`](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)[^1] and DNS name that distributes traffic to a defined set of pods (this is also known as ([load balancing](https://en.wikipedia.org/wiki/Load_balancing_(computing))). **Pods are included in a service by virtue of matching its configured labels.** So the following service, for example, would forward in-cluster requests to `my-cool-service` to pods with the label `app`=`my-cool-app`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-cool-service
spec:
  ports:
  - targetPort: 80
  selector:
    app: my-cool-app
```

### Creating a service with a `ClusterIP`

> If you don't have the `hs-pizza-frontend` pod running, create it by running `kubectl apply -f resources/services/hs-pizza-frontend-pod.yaml`.
{: class=resource }

Because our service is going to target a label, let's give our running `hs-pizza-frontend` pod a sensible label like `app=hs-pizza-frontend` by running `kubectl label pod hs-pizza-frontend app=hs-pizza-frontend`.

Now that our pod is labelled, we can point a service at it, so let's get HyprSk8l's frontend service up and running. The simplest way to expose a service is via `ClusterIP` — in a `ClusterIP` service, Kubernetes DNS will also resolve in-cluster calls to `the-service-name` to that `ClusterIP`. The service manifest will look like this:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: ClusterIP
  ports:
    - name: default
      port: 80
      targetPort: 1234
      protocol: TCP
  selector:
    app: hs-pizza-frontend
```

Paste this YAML into `k8s/frontend-service.yaml` and run `kubectl apply -f k8s/frontend-service.yaml`.

Run `kubectl describe service frontend` and see if there are any `Endpoints` associated with this service. Also note the ClusterIP.

Now, let's test out the different ways of hitting the service. To do this, we're going to launch another pod into the cluster by running `kubectl apply -f resources/utility-pod.yaml`. The utility pod is just something we're using for this workshop; it's not a standard Kubernetes thing.

Get into the utility pod with `kubectl exec -it utility bash` `TODO: install curl on utility image` and then hit the `ClusterIP` that you noted above using `curl`: `curl <CLUSTERIP>:80/pizza`. You can also hit the service by name: `curl frontend/pizza`.

### Adding more pods to the service

A service distributes traffic across all pods that have the appropriate label values. This is useful when you need to scale an app! Let's add a another pod to the frontend service by creating a pod template like so:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hs-pizza-frontend-2
spec:
  containers:
  - name: hs-pizza-frontend-container
    image: ponderosa/hs-pizza-frontend-service:0.1
    imagePullPolicy: Always
    ports:
    - containerPort: 1234
```

You'll note that this is almost exactly the same as the pod we already created, just with a different name. Save it to `k8s/hs-pizza-frontend-pod-2.yaml` and apply it to the cluster with `kubectl apply -f k8s/hs-pizza-frontend-pod-2.yaml`. From within the utility pod, let's run `curl http://frontend/pod_info` to verify that a second pod has joined the service. 

### Creating a `LoadBalancer` service

You'll note that we still cannot access the service we created from _outside_ the cluster. Kubernetes has a first-class way of exposing a service to the wider world: the `LoadBalancer` service. This service will automatically provision a `LoadBalancer` on the underlying cloud provider and rig it up to serve traffic to the Kubernetes service. Note: if you're running on MiniKube, feel free to skip this section, as load-balancing traffic to a VM inside your laptop isn't all that compelling.

To create the `LoadBalancer` service, just add a `type: LoadBalancer` to the service manifest in `k8s/frontend-service.yaml` like so:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: LoadBalancer
  ports:
    - name: default
      port: 80
      targetPort: 1234
      protocol: TCP
  selector:
    app: hs-pizza-frontend
```

Then, update your service by running `kubectl apply -f k8s/frontend-service.yaml`.

## Exercise: create a `ClusterIP` service for the topping suggestion service

> If you don't have a pod running the `topping-suggestion-service` Docker image, create it by running `kubectl apply -f resources/services/hs-pizza-topping-suggestion-service-pod.yaml`.
{: class=resource }

As we've seen, the frontend service depends on the topping suggestion service. Your job is to:

* Label the running pod with `app=hs-pizza-topping-suggestion`
* Create a manifest for a topping suggestion service named "topping-suggestion-service" in `k8s/topping-suggestion-service.yaml`. It should be a ClusterIP service that accepts traffic on port `5678` and forwards traffic to port `5678` (remember, the Dockerfile specifies that `flask` serve traffic on this port). It should point to the pod running the `topping-suggestion-service` image using the label you just added.
* Launch the service into the cluster
* Get the service's `ClusterIP` using `kubectl`
* Hit the service's `/topping_combo` endpoint via its `ClusterIP`
* Hit the service's `/topping_combo` endpoint via itopping suggestion service name
* Visit the frontend service's root page and see if anything's changed!



[^1]: Cluster IPs stay the same for the life of the service.