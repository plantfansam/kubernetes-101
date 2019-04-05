# Lab 2 — Pods and `kubectl create`

## Introduction

HyprSk8l Pizza now has a working Kubernetes cluster! And a Docker container running its front-end web application! Now the question is … how do you get that Docker container running in the Kubernetes cluster? The answer? Pods.

### What's a pod?

Pods are the core of Kubernetes — the legos from which your portable, scalable, and reliable pizza palace will be built. 

> A *Pod* is the basic building block of Kubernetes–the smallest and simplest unit in the Kubernetes object model that you create or deploy. A Pod represents a running process on your cluster.
>
> A Pod encapsulates an application container (or, in some cases, multiple containers), storage resources, a unique network IP, and options that govern how the container(s) should run. A Pod represents a unit of deployment: *a single instance of an application in Kubernetes*, which might consist of either a single container or a small number of containers that are tightly coupled and that share resources.
>
> — [Kubernetes docs](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/)

Pods _may_ contain multiple containers, but you want as few containers per pod as possible. Containers inside a single pod can communicate more easily than containers in separate pods:

>  Containers within a pod share an IP address and port space, and can find each other via `localhost`. They can also communicate with each other using standard inter-process communications...
>
> — [Kubernetes docs](https://kubernetes.io/docs/concepts/workloads/pods/pod/)

Thinking of an application in terms of containers and  `pods` can be a bit of a shift, so don't worry if it doesn't make sense immediately. 

### How do you create and update pods?

Operators use the [`kubectl apply`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands) command to create and update things in the Kubernetes cluster (there is also `kubectl create` — see [these docs](https://kubernetes.io/docs/concepts/overview/object-management-kubectl/overview/) for a discussion of the two). Typically, you run `kubectl apply` and point to a YAML  file specifying what you'd like the cluster to create. This YAML is known as the "manifest." So you might run `kubectl apply -f pod.yaml`, where `pod.yaml` is a manifest looking approximately like:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: python-frontend
spec:
  containers:
  - name: python-frontend-container
    image: my-cool-image:0.1
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

Note: `kubectl apply` is used to create much more than pods — `kubectl` sorts out the objects to be created and then makes requests to the Kubernetes API to apply the specified configuration.

The `kubectl apply` command can accept input from `stdin`, so the following will also work:

  `cat pod.yaml | kubectl apply -f -`

## Prework — Setting up a cluster

This lab assumes you have a running Kubernetes cluster and `kubectl` configured to interact with that cluster. For instructions on doing that, see [our blog post](#todo) or  [lab 1](https://github.com/ponderosa-io/kubernetes-101/tree/master/labs/1-kube-clusters).

## Exercise 0 — Creating a pod with `kubectl apply`

**Tasks:** 

0. Create `pod.yaml`, a manifest for a pod named `hs-pizza-frontend` that runs the Docker image `ponderosa/hs-pizza-frontend:1.0` and serves traffic on port 5000 (`ponderosa/hs-pizza-frontend` is configured to serve traffic on port 5000; you can see how this is configured in this repo's `frontend-python` directory). Note: `ponderosa/hs-pizza-frontend:1.0` is [available on DockerHub](https://cloud.docker.com/u/ponderosa/repository/docker/ponderosa/hs-pizza-frontend).
1. Apply  `pod.yaml` to your Kubernetes cluster. When you run `kubectl get pods`, you should see a running pod with your specified name!
2. Examine the events associated with your pod using `kubectl describe`. Why didn't the pod start immediately?

**Useful docs**: the YAML above, [`kubectl apply`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands), [`kubectl cheat sheet`](https://kubernetes.io/docs/reference/kubectl/cheatsheet/#viewing-finding-resources).

## Exercise 1 — Accessing your pod with port forwarding

Your Kubernetes cluster has security features that prevent anyone on the internet from accessing it without authentication, so you need to configure Kubernetes to serve traffic to your pod (that is, if you want it to receive traffic somehow).  _For development purposes_, we can use the `kubectl port-forward` command to get traffic to its destination; in production, a high-security organization like HyperSk8l Pizza will use Kubernetes services to route traffic to pods (this will be covered in [Lab 3](#todo).[^0] 

**Tasks**: 

0.  Your pod serves traffic on port 5000. Use `kubctl port-forward` to make that port accessible to your host machine on [http//localhost:1234](http//localhost:1234). Visit [http//localhost:1234](http//localhost:1234) — you should see HyprSk8l Pizza's app running.
1.  Hit `control-c` to stop the `kubectl port-forward`.

**Useful docs:** [Kubernetes docs examples](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/#forward-a-local-port-to-a-port-on-the-pod), [`kubectl port-forward`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#port-forward)

## Exercise 2 — Breaking, deleting, and relaunching a pod

`kubectl edit` is used to update API objects that already exist in the cluster. If you're not comfortable with `vim`, you may want to `export EDITOR=nano` before doing this exercise.[^0]

**Tasks**: 

0. With exercise 1's pod still running, use `kubectl edit` to update your pod to use a nonexistent image (e.g. `ponderosa/COBOL-tutorial:1.0`). What happens to the `STATUS` when you run `kubectl get pods`? Can you find the events that result in the pod breaking by using `kubectl describe pod`?
1. Delete your pod using `kubectl delete`.
2. Update your pod to use the original `ponderosa/hs-pizza-frontend:1.0` image and run `kubectl port-forward` to serve traffic. Verify that [http//localhost:1234](http//localhost:1234) works again.

**Useful docs:** [`kubectl edit`](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/#kubectl-edit), [`kubectl delete`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#delete)

## Exercise 3 — Executing commands inside a pod

`kubectl exec` is used to execute commands inside of a container, which lives inside of a pod. It can be used for one-off commands in the pod _or_ can be run in  interactive TTY mode ( using the flags`-it`), which are commonly used to get a shell inside the pod and poke around its container(s).[^0] Getting an interactive shell inside of a container is often referred to as "shelling into a container."

**Tasks:**

0. Make sure you have a `hs-pizza-frontend` pod running from exercise 2. Shell into it using `kubectl exec -it` and make a directory at `/my-cool-directory`. Create two files in `/my-cool-directory` — `my-cool-text-file.txt` and `my-cool-comma-separated-value-file.csv`. Exit your shell, but leave the pod running.
1.  Run `kubectl exec` noninteractively to list the files in `/my-cool-directory`. You should see the files you just created.
2. Delete your pod and then recreate it with `kubectl apply`. Shell in again and look for `/my-cool-directory`. What happened?

**Useful docs:** [get a shell to a running container](https://kubernetes.io/docs/tasks/debug-application-cluster/get-shell-running-container/).

## Exercise 4 — Adding labels and retrieving pods using selectors

In Kubernetes, you can mark objects in the cluster with arbitrary key/value pairs called [`labels`](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/). The command will look something like: `kubectl label object-type object-id labelkey=labelvalue` (a label is a key/value pair.). Labels are incredibly useful when you want to deal with multiple Kubernetes objects as a logical unit, which is an essential feature for megascale web food delivery corporations like Hyprsk8l Pizza. 

You can show the labels attached to a given object by appending `--show-labels` to the `get` command. Labels will also appear if you `kubectl describe` an object. 

**Prework**:

0. Delete all of the pods in your cluster with `kubectl delete --all pods`.
1. This exercise requires two pods. Download another pod definition from this repository by running `wget https://raw.githubusercontent.com/ponderosa-io/kubernetes-101/master/labs/2-pods/resources/utility-pod.yaml`.
2. Launch both pods into the cluster with `kubectl apply -f utility-pod.yaml -f pod.yaml`.

**Tasks:**

0.  Label the `hs-pizza-frontend` pod with `best_topping=broccoli` and the `utility` pod with `best_topping=artichoke`. 
1. Get the labels for all of your pods by running `kubectl get pods --show-labels`. After verifying that the labels are attached with `kubectl get pods —show-labels`, delete all pods.
2. Update your `.yaml` pod definitions to specify the appropriate `best_topping` label and redeploy the pods to your cluster. Verify that it worked with `kubectl get pod --show-labels`.
3. Retrieve all pods that have the `best_topping=broccoli` label using `kubectl get`'s `--selector` option (`-l` is shorthand for the `--selector` flag).

**Useful docs:** [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)

## Exercise 5 — Adding annotation

Kubernetes supports another type of arbitrary key/value pairs: [annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)! They *cannot be used to identify anything using the Kubernetes API* (you can't query on annotations in kubectl), but provide a way to tack information onto Kubernetes objects. Annotation are useful for third-party tooling, beta features, and more. When creating an annotation, it's customary to include a prefix on the key to avoid collisions[^0]

**Tasks**:

0. Annotate a `node` in your cluster with the completely ludicrious label `best_topping=ham` using `kubectl annotate`. Verify that it worked with `kubectl describe`.
1. Delete the `hs-pizza-frontend` pod and then modify `pod.yaml` to specify the equally ludicrous label `best_topping=pineapple`. Launch it into the cluster and verify its presence with `kubectl describe`.[^0]

## Followup Exercises

0. Follow the exercise 4 prework, and then
   1. Retrieve any pods that have the `best_topping` label using the `--selector` option.
   2. Retrieve all pods that have _any_ value for the `best_pasta_shape` label.

**Useful docs:** [`kubectl annotate`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#annotate)

[^0]: Port forwarding is a magical and awesome thing, but it's beyond the scope of this lab; you can read more [here](https://en.wikipedia.org/wiki/Port_forwarding). 
[^0]: Note: `kubectl edit` isn't a  maintainable workflow, as your running workloads will drift from what's specified in your YAML. Generally if your pod's configuration is busted, it's good practice to delete it, update the YAML that generated it, and create an entirely new pod with `kubectl create -f`.
[^0]: Wondering what a TTY is? It's a teletypewriter and it's both important to accessibility _and_ an awesome bit of computing history. See: https://askubuntu.com/a/481919.
[^0]: As an example: imagine an engineer working on the same cluster and decide to annotate one of their nodes with `active=true` for whatever reason. Then, they hook up some cluster automation software that _also_ tries to label that node with `active=true`. The annotation would error out! This could have been avoided if the application engineer had annotated the node with `mycoolcompany./active=true` and/or the automation software provider used the annotation `mycoolautomationcompany.rodeo/active=true`
[^0]: Note that there is both a `best_topping` _annotation_ and a `best_topping` _label_; setting aside the epistemological absurdity of having two favorite toppings, it's important to note that this is possible. You can't have two labels or annotations with the same key.