# Lab 2 — Pods and `kubectl create`

## Introduction

### What's a pod 

Pods are the core of Kubernetes — the legos from which your portable, scalable, and reliable software palace will be built. 

> A *Pod* is the basic building block of Kubernetes–the smallest and simplest unit in the Kubernetes object model that you create or deploy. A Pod represents a running process on your cluster.
>
> A Pod encapsulates an application container (or, in some cases, multiple containers), storage resources, a unique network IP, and options that govern how the container(s) should run. A Pod represents a unit of deployment: *a single instance of an application in Kubernetes*, which might consist of either a single container or a small number of containers that are tightly coupled and that share resources.
>
> — [Kubernetes docs](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/)

Pods _may_ contain multiple containers, but you want as few containers per pod as possible. Containers inside a single pod can communicate more easily than containers in separate pods:

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

| key             | meaning                                                      |
| --------------- | ------------------------------------------------------------ |
| `apiVersion`    | the [API group](https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-groups) supporting the `kind` |
| `kind`          | the API resource to be created                               |
| `metadata`      | metadata about the API resource to be created                |
| `containers`    | the containers inside the pod                                |
| `name`          | the name of the container (this is different than the pod name) |
| `image`         | the image to base the container on                           |
| `containerPort` | the port that the container's application will respond to    |

Note: `kubectl create` is used to create more than pods — the Kubernetes API sorts out what should be created based on the configuration passed in. 

The `kubectl create` command can accept input from `stdin`, so the following will also work:

  `cat pod.yaml | kubectl create`

## Prework — Setting up a  cluster

This lab assumes you have a running Kubernetes cluster and `kubectl` configured to interact with that cluster. For instructions on doing that, see [lab 1](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/1-kube-clusters).

## Exercise 0 — Creating a pod with `kubectl create`

In [lab 0](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/0-docker), you created a Docker image and pushed it to DockerHub, and in [lab 1](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/1-kube-clusters) you created a cluster and configured `kubectl`. Now, we're going to do things in the cluster!

**Tasks:** 

0. Create a YAML manifest for a pod that runs your Docker image
1. Run that pod in your Kubernetes cluster

**Useful docs**: the YAML above, [`kubectl create`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands) 

**Shortcuts**: if you haven't built the Docker image from [lab 0](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/0-docker), you can use the container image  `ponderosa/kubernetes-101-frontend:0.1`

**Check your work:** when you run `kubectl get pods`, you should see a running pod with your specified name!

## Exercise 1 — Accessing your pod with port forwarding

In production, you won't use `kubectl port-forward` to access running pods over HTTP, but in this tutorial, you will! Port forwarding is a magical and awesome thing, but it's beyond the scope of this lab; you can read more [here](https://en.wikipedia.org/wiki/Port_forwarding). 

**Tasks**: 

0.  Make your pod's port `8080` accessible to your host machine on [http//localhost:1234](http//localhost:1234)

**Useful docs:** [Kubernetes docs examples](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/#forward-a-local-port-to-a-port-on-the-pod), [`kubectl port-forward`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#port-forward)

**Check your work**: visit [http//localhost:1234](http//localhost:1234) — you should see our app running.

## Exercise 2 — Breaking, fixing, and deleting a pod

`kubectl edit` is used to update API objects that already exist in the cluster. If you're not comfortable with `vim`, you may want to `export EDITOR=nano` before doing this exercise.[^0]

**Tasks**: 

0. Update your pod to use a nonexistent image (e.g. `ponderosa/COBOL-tutorial:1.0`). This should break [http//localhost:1234](http//localhost:1234). Note the change in `STATUS` in `kubectl get pods`.
1. Update your pod to use the old image and verify that [http//localhost:1234](http//localhost:1234) works again.
2. Delete your pod. Verify that http://localhost:1234 is broken again.

**Useful docs: ** [`kubectl edit`](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/#kubectl-edit), [`kubectl delete`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#delete)

## Exercise 3 — Adding and retrieving by label

In Kubernetes, you can mark objects in the cluster with arbitrary key/value pairs called [`labels`](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/).  `kubectl label object-type object-id labelkey=labelvalue` (a label is a key/value pair.). They are incredibly useful when you want to deal with multiple Kubernetes objects as a logical unit (you just wait!). You can show the labels attached to a given object by appending `--show-labels` to the `get` command. Labels will also appear if you `kubectl describe` an object. 

**Tasks:**

0. Redeploy your pod to your Kubernetes cluster (use the same steps as exercise 0)
1. Add 



[^0] Note: `kubectl edit` isn't a  maintainable workflow, as your running workloads will drift from what's specified in your YAML. Generally if your pod's configuration is busted, it's good practice to delete it, update the YAML that generated it, and create an entirely new pod with `kubectl create -f`.

