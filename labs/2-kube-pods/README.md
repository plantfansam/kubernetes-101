# Lab 2 - Pods and `kubectl create`

## Introduction

### What's a pod 

Pods are the core of Kubernetes — the legos from which your portable, scalable, and reliable software palace will be built. 

> A *Pod* is the basic building block of Kubernetes–the smallest and simplest unit in the Kubernetes object model that you create or deploy. A Pod represents a running process on your cluster.
>
> A Pod encapsulates an application container (or, in some cases, multiple containers), storage resources, a unique network IP, and options that govern how the container(s) should run. A Pod represents a unit of deployment: *a single instance of an application in Kubernetes*, which might consist of either a single container or a small number of containers that are tightly coupled and that share resources.
>
> — [Kubernetes docs](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/)

Pods _may_ contain multiple containers, but you want as few containers per pod as possible (in other words: one). Containers inside a single pod can communicate more easily than containers in separate pods:

>  Containers within a pod share an IP address and port space, and can find each other via `localhost`. They can also communicate with each other using standard inter-process communications...
>
> — [Kubernetes docs](https://kubernetes.io/docs/concepts/workloads/pods/pod/)

Thinking of an application in terms of containers and  `pods` can be a bit of a shift, so give yourself a bit of time to experiment. 

### How do you create and update pods?

Operators use the [`kubectl create`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands) command to, well, `create` things in the Kubernetes cluster. Operators  usually use `kubectl create` with a YAML  file containing configuration. This YAML is known as the "manifest." So they would run `kubectl create -f pod.yaml`, where `pod.yaml` is a manifest looking approximately like:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: kubernetes-101-frontend
spec:
  containers:
  - name: frontend-container
    image: my-cool-image:0.0.0
    ports:
    - containerPort: 5678
```

Let's break this down:

`apiVersion`: the [API group](https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-groups) supporting the `kind` 

`kind`: the API resource to be created

`metadata`: metadata about the API resource to be created

`containers`: the containers inside the pod

​	`name`: the name of the container (this is different than the pod name)

​	`image`: the image to base the container on

​	`containerPort`: the port that the container's application will respond to

Note: `kubectl create` is used to create more than pods — the Kubernetes API sorts out what should be created based on the configuration passed in. 

The `kubectl create` command can accept input from `stdin`, so the following will also work:

  `cat pod.yaml | kubectl create`

## Exercise 0 — Creating a pod with `kubectl create`

Operators use the [`kubectl create`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands) command to, well, `create` things in the Kubernetes cluster. The command can accept input from `stdin`, so the following would work if `mycoolconfig` was actually a valid configuration string:

  `echo "mycoolconfig" | kubectl create`

Operators more commonly target a `yaml` containing configuration (for example)

Note: `kubectl create` is used to create more than pods — the Kubernetes API sorts out what should be created based on the configuration passed in.