# Lab 1 - Introducing Kubernetes Clusters and `kubectl`

## Introduction

Now that HyprSk8l Pizza has containerized its application, it's time to move it onto Kubernetes. In order to put a workload onto Kubernetes, you need to have a Kubernetes installation, which is known as a "cluster" (a "cluster" because the installation is frequently on more than one machine). You can think of a cluster as an independent instance of Kubernetes. In the future, HyprSk8l's engineering organization may need several clusters, but for now, we'll just have one. 

## Prework — Setting up a cluster

If you're a [Ponderosa](https://ponderosa.io) workshop participant, you should already have a Kubernetes cluster set up for you — talk to your instructor if you don't. If you're doing this outside of a workshop, you can create a cluster on whichever cloud provider you want, or use [Minikube](https://kubernetes.io/docs/setup/minikube/), which lets you run a one-node Kubernetes cluster on your local machine.[^0]  To create a cluster on [Digital Ocean](https://www.digitalocean.com/) (they offer a free $100 credit for new users), check out our blog post [here](#todo).

## Exercise 0 — Configuring `kubectl`

Operators issue commands to the Kubernetes cluster using its HTTP API, frequently through the [`kubectl`](https://kubernetes.io/docs/reference/kubectl/overview/) command line utility. In order to use `kubectl`, you must [install it](https://kubernetes.io/docs/tasks/tools/install-kubectl/) and [configure it to look at your cluster](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/) — this is done by placing a configuration file wherever your `KUBECONFIG` environment variable points to (`~/.kube/config` by default). If you're a [Ponderosa](https://ponderosa.io) workshop participant, you should already have access to this file. If you just set up your cluster on Digital Ocean, you can use the [`/kubeconfig`](https://developers.digitalocean.com/documentation/v2/#retrieve-the-kubeconfig-for-a-kubernetes-cluster) endpoint to get your configuration file:

```bash
curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer mycooldigitaloceantoken" "https://api.digitalocean.com/v2/kubernetes/clusters/mycoolclusterid/kubeconfig" > ~/.kube/config)
```

**Tasks**: 

0. Figure out the URLs at which Kubernetes master and CoreDNS are running in your Kubernetes cluster using [kubectl cluster-info](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#cluster-info). 

**Useful docs:** [access a cluster](https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/), [configure access to multiple clusters](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/), [kubectl cluster-info](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#cluster-info).

## Exercise 1 — Exploring your cluster

`kubectl` has some commands oriented around ascertaining the overall health of your cluster. They're not often used, but can be helpful in diagnosing problems.

**Tasks:** 

0. Figure out which version of `kubectl` you're running, and which version of Kubernetes your cluster is running.
1. Determine how many nodes are in your kubernetes cluster.

**Useful docs**: [`kubectl version`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#version), [`kubectl` resource types](https://kubernetes.io/docs/reference/kubectl/overview/#resource-types), [`kubectl get`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get)

## Exercise 2 — Getting information about objects

`kubectl get` is used to explore different Kubernetes *objects*, such as [pods](https://kubernetes.io/docs/concepts/workloads/pods/pod/), [jobs](https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/), [nodes](https://kubernetes.io/docs/concepts/architecture/nodes/), and [namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/).

**Tasks:** 

0. List every namespace in your kubernetes cluster.
1. List every node in your kubernetes cluster.
2. List the `pods` in the `kube-system` namespace (they're there, we promise!) .

**Useful docs**: [`kubectl get`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get), [Kubernetes namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

## Exercise 3 — Digging into API objects

While `kubectl get` can give you good information about different objects in your cluster, you sometimes want more information. `kubectl describe` is great for that. To get more information about the `foobar` pod, for example, you might run `kubectl describe pod foobar`, where `foobar` is a unique identifier for the `pod`

**Tasks:**

0. Find the `InternalIP`, `ExternalIP`, and `Host OS` of one node in your cluster.
1. Find any applicable resource limits on the `kube-system` namespace. 

Useful docs: [`kubectl describe`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#describe)

## Exercise 4 — Getting help

`kubectl --help` gets you top-level information on various `kubectl` subcommands (like `kubectl get`; `get` is the "subcommand" here). For more information on a subcommand, run `--help` against the subcommand (e.g. `kubectl get --help`) .

**Tasks**:

0. Get a list of your cluster's nodes in `json`.
1. Use the `explain` subcommand to learn what a `service` is. 
2. Bookmark the Kubernetes [concepts docs](https://kubernetes.io/docs/concepts/), [API reference docs](https://kubernetes.io/docs/reference/#api-reference), and [`kubectl` reference docs](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands) in your browser. Take a moment to poke around each one.

**Useful docs:** [`kubectl get`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get), [`kubectl` operations](https://kubernetes.io/docs/reference/kubectl/overview/#operations)

[^0]: There is software to manage multiple Kubernetes clusters. See, e.g. [Rancher](https://rancher.com/).
[^1]: Most cloud providers provide Kubernetes as a service, but if you're interested in setting up your own, try [Kubernetes the hard way](https://github.com/kelseyhightower/kubernetes-the-hard-way). 