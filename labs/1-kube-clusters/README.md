# Lab 1 - Introducing Kubernetes Clusters and `kubectl`

## Introduction

A Kubernetes installation — which frequently takes place on more than one machine — is known as a "cluster." You can think of a cluster as an independent instance of Kubernetes. One organization may have many clusters, and there's software to manage running them (see, e.g. [Rancher](https://rancher.com/); we won't be using Rancher for this lab).

This lab assumes you have a cluster set up already. If you don't, most cloud providers offer a managed Kubernetes service. You can also use `terraform` to set up a cluster on Digital ocean, which offers $100 in free credit for new users — check out [Ponderosa's blog post]() for more info on that.

## Prework 0 — Setting up a cluster

If you're a [Ponderosa](https://ponderosa.io) workshop participant, you should already have a Kubernetes cluster set up for you — check your email for details. If you're doing this outside of a workshop, you can create a cluster on whichever cloud provider you want, or use [Minikube](https://kubernetes.io/docs/setup/minikube/), which lets you run a one-node Kubernetes cluster on your local machine.[^0]  To create a cluster on [Digital Ocean](https://www.digitalocean.com/), you can run `terraform apply` from this directory (you'll need to [get a Digital Ocean account (and $100 of free credit!)](https://try.digitalocean.com/performance/) and [install `terraform`](https://learn.hashicorp.com/terraform/getting-started/install.html) first).

## Exercise 0 — Configuring `kubectl`

You frequently use the [`kubectl`](https://kubernetes.io/docs/reference/kubectl/overview/) command to interact with a Kubernetes cluster. In order to use `kubectl`, you must [configure it to look at your cluster](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/) — this is done by placing a configuration file wherever your `KUBECONFIG` environment variable points to (`~/.kube/config` by default). If you're a [Ponderosa](https://ponderosa.io) workshop participant, you should already have access to this file. If you just set up your cluster on Digital Ocean, you can use the [`/kubeconfig`](https://developers.digitalocean.com/documentation/v2/#retrieve-the-kubeconfig-for-a-kubernetes-cluster) endpoint to get your configuration file:

```bash
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer mycooldigitaloceantoken" "https://api.digitalocean.com/v2/kubernetes/clusters/mycoolclusterid/kubeconfig" > ~/.kube/config)
```

**Task**: Figure out the URLs at which Kubernetes master and CoreDNS are running in your Kubernetes cluster using [kubectl cluster-info](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#cluster-info). 

**Useful docs:** [access a cluster](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/), [configure access to multiple clusters](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/), [kubectl cluster-info](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#cluster-info).

**Check your work**: there are no automated checkers for these tasks.

## Exercise 1 — Exploring your cluster

`kubectl` has some commands oriented around ascertaining the overall health of your cluster. They're not often used, but can be helpful in diagnosing problems.

**Tasks:** 

0. figure out which version of `kubectl` you're running, and which version of Kubernetes your cluster is running
1. get the status of the Kubernetes cluster's `scheduler`, `controller-manager`, and `etcd` components
2. determine how many nodes are in your kubernetes cluster

**Useful docs**: [`kubectl version`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#version), [`kubectl resource types`](https://kubernetes.io/docs/reference/kubectl/overview/#resource-types), [`kubectl get`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get)

**Check your work**: there are no automated checkers for these tasks.

## Exercise 2 — Getting information about objects

`kubectl get` is used to explore different Kubernetes *objects*, such as [pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/), [jobs](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/), [nodes](https://kubernetes.io/docs/concepts/architecture/nodes/), and [namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/).

**Tasks:** 

0. List every namespace in your kubernetes cluster
1. List every node in your kubernetes cluster
2. List the `pods` in the `kube-system` namespace (they're there, I promise!) 

**Useful docs**: [`kubectl get`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get), [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

**Check your work**: there are no automated checkers for these tasks.

## Exercise 3 — Digging into API objects

While `kubectl get` can give you good information about different objects in your cluster, you sometimes want more information. `kubectl describe` is great for that. To get more information about the `foobar` pod, for example, you might run `kubectl describe pod foobar`, where `foobar` is a unique identifier for the `pod`

**Tasks:**

0. Find the `InternalIP`, `ExternalIP`, and `Host OS` of each node in your cluster
1. Find any applicable resource limits on the `kube-system` namespace. 

Useful docs: [`kubectl describe`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe)

**Check your work**: there are no automated checkers for these tasks.

## Exercise 4 — Getting help

`kubectl --help` gets you top-level information on various `kubectl` subcommands (like `kubectl get`; `get` is the "subcommand" here). For more information on a subcommand, run `--help` against the subcommand (e.g. `kubectl get --help`) .

**Tasks**:

0. Get a list of your cluster's nodes in `json`.
1. Use the `explain` subcommand to learn what a `service` is. 
2. Bookmark the Kubernetes [concepts docs](https://kubernetes.io/docs/concepts/) and [reference docs](https://kubernetes.io/docs/reference/#api-reference) in your browser. Take a moment to poke around each one.

Useful docs: [`kubectl get`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get), [`kubectl` operations](https://kubernetes.io/docs/reference/kubectl/overview/#operations)

[^0]: Most cloud providers provide Kubernetes as a service, but if you're interested in setting up your own, try [Kubernetes the hard way](https://github.com/kelseyhightower/kubernetes-the-hard-way). 