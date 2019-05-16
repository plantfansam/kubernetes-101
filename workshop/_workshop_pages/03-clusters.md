---
layout: workshop-page
title: "Kubernetes Clusters"
---

Now that we've containerized HyprSk8l Pizza's services, it's time to move onto Kubernetes! In order to put a workload onto Kubernetes, we'll first need to have a Kubernetes installation, which is known as a "cluster" (a "cluster" because the installation is frequently on more than one machine). You can think of a cluster as an independent instance of Kubernetes. In the future, HyprSk8l's engineering organization may need several clusters, but for now, we'll just have one. 

## Kubernetes cluster overview

At its core, the Kubernetes workflow goes like this: you tell the Kubernetes cluster that you want it to run an app with certain parameters (a Docker image, a specific command to run in that Docker image, networking information about how different containers can find one another, and so on). Here's an admittedly crude depiction:

![Architecture diagram](kubernetes-top-level.jpg)

As you can see, you talk to the Kubernetes API to ask it to do work. Seems kind of magical, right? Yes. There's a lot going on beneath that silky smooth API. You don't need to understand too much about a Kubernetes cluster's architecture at this point, but it's very helpful vocabulary to know. Here's an admittedly crude diagram of the architecture of a Kubernetes cluster:

![Cluster architecture diagram](kubernetes-cluster-diagram.jpg)

As a Kubernetes user, you're typically talking to the Kubernetes API, which is part of the _cluster control plane_. The cluster control plane maintains an understanding of what _should_ be running — based on Kubernetes' own application requirements and what cluster users have told it to do — and orchestrates the cluster such that what _should_ be running _is_ running.

### What's a node?

A node is just a server that's part of the Kubernetes cluster.

### What's the cluster control plane doing?

The cluster control plane maintains knowledge of the state of the cluster using the **cluster state store**, which is an [etcd](https://github.com/etcd-io/etcd) instance. This knowledge is required for it to do its job (otherwise you might start multiple instances of the same application, etc.). The **API server** handles inbound requests made to the cluster; the API is used both by in-cluster components and by its end users. The **scheduler** finds nodes for pods (which wrap containers) that need a place to run. The **controller-manager server** does a whole lot behind the scenes; too much to talk about right now, but check out this [Kubernetes architecture doc](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/architecture/architecture.md#the-kubernetes-node) for details.

### What are the worker nodes doing?

The worker nodes, as you might imagine, are doing work! There's a few components to that. First, there is the **kubelet**. The Kubelet is a Kubernetes agent that runs on every node (which, in fact, is a node by virtue of it running the kubelet!). The worker nodes do work by running containers on their **container runtime**. This container runtime can be Docker, containerd, cri-o, or anything else that implements the Kubernetes Container Runtime Interface. Finally, the **Kube proxy** runs on every worker node to help workloads find and connect to one another.

**Useful docs**:

## Setting up a cluster

If you're a [Ponderosa](https://ponderosa.io) workshop participant, you should already have a Kubernetes cluster set up for you — talk to your instructor if you don't. If you're doing this outside of a workshop, you can create a cluster on whichever cloud provider you want, or use [Minikube](https://kubernetes.io/docs/setup/minikube/), which lets you run a one-node Kubernetes cluster on your local machine. For instructions on creating a cluster on [Digital Ocean](https://www.digitalocean.com/) (they offer a free $100 credit for new users), check out our blog post [here](https://ponderosa.io/blog/kubernetes/2019/03/13/terraform-cluster-create/).

## Installing Kubectl

Operators issue commands to the Kubernetes cluster using its HTTP API, frequently through the [`kubectl`](https://kubernetes.io/docs/reference/kubectl/overview/) command line utility. In order to use `kubectl`, you must [install it](https://kubernetes.io/docs/tasks/tools/install-kubectl/) and [configure it to look at your cluster](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/) — this is done by placing a configuration file wherever your `KUBECONFIG` environment variable points to (`~/.kube/config` by default). If you're a [Ponderosa](https://ponderosa.io) workshop participant, you should already have access to this file. If you just set up your cluster on Digital Ocean, you can use the [`/kubeconfig`](https://developers.digitalocean.com/documentation/v2/#retrieve-the-kubeconfig-for-a-kubernetes-cluster) endpoint to get your configuration file:

```bash
curl -X GET -H "Content-Type: application/json" \
    -H "Authorization: Bearer mycooldigitaloceantoken" \
    "https://api.digitalocean.com/v2/kubernetes/clusters/mycoolclusterid/kubeconfig" \
    > ~/.kube/config)
```

**Useful docs:** [access a cluster](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/), [configure access to multiple clusters](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/), [kubectl cluster-info](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#cluster-info).

## Exploring kubectl and the cluster

Once you have `kubectl` configured you can do a lot of cool stuff, like figuring out which version of `kubectl` you're running and which version of Kubernetes the cluster is running (do this with `kubectl version`). You can see more info about your kubernetes cluster with `kubectl cluster-info`.

### `kubectl` get

`kubectl get` is used to explore different Kubernetes *objects*, such as [pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/), [jobs](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/), [nodes](https://kubernetes.io/docs/concepts/architecture/nodes/), and [namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/). You list all of the resources in your currently configured namespace with the command `kubectl get <resourcename>`. Try running `kubectl get nodes` to see all the nodes in your cluster.

### `kubectl describe`

While `kubectl get` can give you good information about different objects in your cluster, you sometimes want more information. `kubectl describe` is great for that. To get more information about the `foobar` pod, for example, you might run `kubectl describe pod foobar`, where `foobar` is a unique identifier for the `pod`. The formula for `kubectl describe` is, generally speaking `kubectl describe object-type object-identifier`. So to check out details of your node with name minikube, you'd run `kubectl describe node minikube`.

### Getting help

`kubectl --help` gets you top-level information on various `kubectl` subcommands (like `kubectl get`; `get` is the "subcommand" here). For more information on a subcommand, run `--help` against the subcommand (e.g. `kubectl get --help`).

You can also use `kubectl explain` to get more information about different concepts — try running `kubectl explain service`.