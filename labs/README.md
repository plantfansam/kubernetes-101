# Labs — Introduction

After doing an initial deployment on hand-configured [EC2](https://aws.amazon.com/ec2/) instances, the engineering team at [HyprSk8l Pizza](#todo) has decided to serve its application on Kubernetes. It's not just that Kubernetes is all the rage; they're wise to its benefits:

- Scaling the application is important (important for a HyprSkale application)
- Kubernetes makes service discovery trivial
- Containerizing the application allows for more efficient resource utilization
- And more!

These labs will cover their journey to a Kubernetes-ized application!

## Lab Overview

The labs are divided by subject matter. They are not intended to be comprehensive, but include links and followup exercise for students that are interested in digging deeper.

0. [Docker](#todo) — covers Docker, the world's dominant containerization technology.
1. [Clusters](#todo) — covers Kubernetes clusters (a "cluster" is the name of the thing that you deploy your application on; it is a set of interconnected servers running the Kubernetes platform).
2. [Pods]() — covers the basic building block of Kubernetes application deployments, along with how to update and label them.
3. [Services](#todo) — covers Kubernetes services, which group pods into units to facilitate interaction.
4. [ReplicaSets](#todo) — covers replicaSets, which ensure that the cluster is running a specific number of a designated pod.
5. [Deployments](#todo) — covers deployments, which are how Kubernetes manages the rollout of new versions of an application.
6. [Namespaces](#todo) — covers Kubernetes namespaces, which divide a cluster into multiple "virtual clusters."
7. [ConfigMaps and Secrets](#todo) — covers configuration management through the Kubernetes concepts of `configMaps` and `secrets` (typically, you use `ConfigMaps` and `Secrets` to pass configuration information into pods).