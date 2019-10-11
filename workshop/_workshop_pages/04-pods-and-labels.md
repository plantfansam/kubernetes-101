---
layout: workshop-page
title: "Pods, Labels, and Annotation"
---

Assuming you completed [the Kubernetes cluster section]({{ site.baseurl }}/03-clusters), you now have a working Kubernetes cluster that we can use for HyperScale Pizza's big Kubernetes migration! And Docker images that can run both the webapp service and the topping suggestion combo service! Now the question is … how do you get those Docker images running in the Kubernetes cluster? The answer? Pods.

#### What's a pod?

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

### Creating a webapp service pod

Kubernetes operators use the [`kubectl apply`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands) command to create and update things in the Kubernetes cluster (there is also `kubectl create` — see [these docs](https://kubernetes.io/docs/concepts/overview/object-management-kubectl/overview/) for a discussion of the two). Typically, you run `kubectl apply` and point to a YAML file specifying what you'd like the cluster to create. This YAML is known as the "manifest." So you might run `kubectl apply -f pod.yaml`, where `pod.yaml` is a manifest looking approximately like:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: the-name-of-my-amazing-pod
spec:
  containers:
  - name: my-containers-name-is-potato
    image: my-dockerhub-account/my-cool-image:0.1
    ports:
    - containerPort: 5678
```

There's a couple of really important bits of configuration here. First is the `image`, which tells Kubernetes what image you want to run (it will look on DockerHub by default). Next is the `ports` stanza, which tells Kubernetes how to map traffic going to the _pod_, which wraps the container, to the _container_, which  actually runs the application. In this sample, we're saying that the container's port `5678` should be exposed to pod traffic.

To get our webapp service pod into Kubernetes, we first need to define a manifest. It'll look like this:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hs-pizza-webapp
spec:
  containers:
  - name: hs-pizza-webapp-container
    image: ponderosa/hs-pizza-webapp:latest
    imagePullPolicy: Always
    ports:
    - containerPort: 1234
```

Create a file called `hs-pizza-webapp-pod.yaml` in the `k8s/` directory and paste in the above YAML. Remember that we specified that our webapp flask appplication would run on port `1234` in the container image we created in [the containerization module]({{ site.baseurl }}/02-containerization). Once you've added this YAML file, create it in the cluster by running `kubectl apply -f k8s/hs-pizza-webapp-pod.yaml`. Now, check and see what's running in the cluster with `kubectl get pods`. You can get more details about the pod you just created with `kubectl describe pod hs-pizza-webapp`.

### Accessing your pod with port forwarding

Now that our Kubernetes pod is running, how do we get to it? Our Kubernetes cluster has security features that prevent anyone on the internet from accessing pods without authentication, so we need to configure Kubernetes to serve traffic to our pod (that is...it has to get web requests somehow).

_For development purposes_, we can use the `kubectl port-forward` command to get traffic to its destination. Port forwarding is used for convenience's sake, but is not intended for use in production contexts! In production, a high-security organization like HyperSk8l Pizza will use Kubernetes services to route traffic to pods (this will be covered a bit later in the workshop.[^1]

Run `kubectl port-forward hs-pizza-webapp 5000:1234` to forward localhost:5000 to port `1234` in the pod. Hit `http://localhost:5000/pod-info` and check out where your pod's running from!

### Getting logs from a running pod

Our application is configured to log to `STDOUT`, and containers' `STDOUT` streams are collected by Kubernetes so we can view them. To view the logs for the pod that we just created, run `kubectl logs -f hs-pizza-webapp` (the `-f` flag follows the logs so that when new stuff is logged, it goes straight to your terminal). These logs are available in real-time, so if you're tailing the logs and then visit the web app in your browser, you should see your request info pop up in your terminal (I'd recommend appending the querystring `?hi_mom=true`). 

Once you're sufficiently wowwed, you can hit ctrl+c to stop port forwarding.

### Breaking, deleting, and relaunching a pod

`kubectl edit` is used to update API objects that already exist in the cluster. It will automatically open up your terminal's default text editor when you run the command, so if you're not comfortable with `vim`, you may want to `export EDITOR=nano` before continuing.[^2] 

Once you've done that, let's edit our `hs-pizza-webapp` pod with `kubectl edit pod hs-pizza-webapp`. Update the YAML so that it points to a nonexistent image (add a character somewhere or get more creative then that) and save your changes (`:wq` in vim, if you're using that). Stand up, walk around for a minute, and when you come back, check out what happened to the pods in your cluster by runing `kubectl get pods`. If you describe the pod again, you'll see that Kubernetes could not find the specified docker image:

```
$ kubectl describe pod hs-pizza-webapp

Events:
  Type     Reason     Age                From                       Message
  ----     ------     ----               ----                       -------
  ...
  ...
  Normal   Killing    2m6s               kubelet, worker-pool-x76v  Container hs-pizza-webapp-container definition changed, will be restarted
  Normal   Pulling    56s (x3 over 96s)  kubelet, worker-pool-x76v  Pulling image "ponderosa/hs-pizza-webappeee:latest"
  Warning  Failed     56s (x3 over 96s)  kubelet, worker-pool-x76v  Failed to pull image "ponderosa/hs-pizza-webappeee:latest": rpc error: code = Unknown desc = Error response from daemon: pull access denied for ponderosa/hs-pizza-webappeee, repository does not exist or may require 'docker login'
``` 

Once you're sufficiently satisfied that your pod is broken, you can delete your pod with `kubectl delete hs-pizza-webapp`.

### Executing commands inside a pod

`kubectl exec` is used to execute commands inside of a container, which, you'll remember, are always housed inside of pods. `kubectl exec` can be used for one-off commands in the pod _or_ can be run in interactive TTY mode ( using the flags`-it`), which are commonly used to get a shell inside the pod and poke around its container(s).[^2] Getting an interactive shell inside of a container is often referred to as "shelling into a container."

Let's start by recreating our pod with `kubectl apply -f k8s/hs-pizza-webapp-pod.yaml`. We'll re-establish the port-forwarding with `kubectl port-forward hs-pizza-webapp 5000:1234`. Now, we'll check out the `/ls_tmp` endpoint, which lists the contents of the `/tmp` directory in the pod. Do that by running `curl localhost:5000/ls_tmp`. Don't ask why HyperScale pizza has this feature!!!

```
$ curl localhost:5000/ls_tmp
Listing files in /tmp on HOSTNAME hs-pizza-webapp:
[]
```

Now, open up another terminal window  and shell into the pod by running  `kubectl exec -it hs-pizza-webapp bash`. Make some files in the `/tmp` directory with `touch /tmp/whatever` and then `exit` to get out of the pod.

`curl` the `ls_tmp` endpoint again — you should see your file(s)!

```
$ curl localhost:5000/ls_tmp
Listing files in /tmp on HOSTNAME hs-pizza-webapp:
['whatever', 'wat']
```

### Adding labels and retrieving pods using selectors

In Kubernetes, you can mark objects in the cluster with arbitrary key/value pairs called [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/). The command will look something like: `kubectl label object-type object-id labelkey=labelvalue` (a label is a key/value pair). Labels are incredibly useful when you want to deal with multiple Kubernetes objects as a logical unit, which is an essential feature for planet-scale web food topping suggestion apps like HyperScale Pizza. 

Let's start our labelling process by launching a second pod into the cluster. Run `kubectl apply -f resources/utility-pod.yaml` to launch a pre-defined pod (feel free to take a look at that pod's manifest — it's pretty boring).

Next, run `kubectl get pods --show-labels` to show the different pods' labels. It's a travesty that `hs-pizza-webapp` doesn't have a `best-pasta-shape` label. We'll add one by running `kubectl label pod hs-pizza-webapp best_pasta_shape=penne`.

Instead of labeling pods by hand, it's often helpful to express labels in the pod manifest. Update the YAML manifest (which we put in `k8s/hs-pizza-webapp-pod.yaml`) for the pizza webapp pod to define this label:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hs-pizza-webapp
  labels:
    best_pasta_shape: penne
spec:
  containers:
  - name: hs-pizza-webapp-container
    image: ponderosa/hs-pizza-webapp:latest
    imagePullPolicy: Always
    ports:
    - containerPort: 1234
```

Apply the changed manifest by running `kubectl apply -f k8s/hs-pizza-webapp-pod.yaml`:

```
$ kubectl apply -f k8s/hs-pizza-webapp-pod.yaml
pod/hs-pizza-webapp configured
```

Note that `kubectl apply` _modified the existing pod_ rather than creating a whole new one.

Now we can make sure that the pod was modified by running `kubectl get pods --show-labels`:

```
$ kubectl get pods --show-labels
NAME              READY   STATUS    RESTARTS   AGE     LABELS
hs-pizza-webapp   1/1     Running   0          16m     best_pasta_shape=penne
utility           1/1     Running   0          2m55s   best_pasta_shape=rigatoni
```

#### Fetching pods by label

Sometimes it's useful to fetch pods with certain labels. If you have hundreds of pods running in a cluster and you want to filter them by their app (or possibly which pasta shape the app thinks is the best), you can do that by supplying `-l labelname=labelvalue` when running `kubectl get pods`. So to get all of the pods with the label `best_pasta_shape=rigatoni`, we'll run the following:

```
$ kubectl get pods -l best_pasta_shape=rigatoni
NAME      READY   STATUS    RESTARTS   AGE
utility   1/1     Running   0          7m11s
```

While this is very useful for people using Kubernetes clusters, it's also very useful when scripting and creating services, which we'll cover in [the next section]({{ site.baseurl }}/05-services).

### Adding annotation

Kubernetes supports another type of arbitrary key/value pairs: [annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)! They *cannot be used to identify anything using the Kubernetes API* (i.e. you can't easily query pods based on annotations in `kubectl`), but provide a way to tack information onto Kubernetes objects. Annotation are useful for third-party tooling, beta features, and more. 

As with labels, you can annotate a lot of different things in Kubernetes. Let's apply the completely ludicrous annotation `best_pizza_topping=ham` to one the nodes in our cluster. First, we'll get all of the nodes:

```
$ kubectl get nodes
NAME               STATUS   ROLES    AGE     VERSION
worker-pool-x76v   Ready    <none>   6h58m   v1.14.2
```

Note: I'm running a one-node cluster to save money.

Now, we can annotate the node as follows:

```
kubectl annotate node worker-pool-x76v best_pizza_topping=ham
node/worker-pool-x76v annotated
```

Checking out the node's description verifies that it was applied:

```
$ kubectl describe node worker-pool-x76v | grep best_pizza_topping
Annotations:        best_pizza_topping: ham
```

Building on the best practice of annotating every object with an opinion about the best pizza topping, let's add a `best_pizza_topping` annotation to the pod manifest in `k8s/hs-pizza-webapp-pod.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hs-pizza-webapp
  labels:
    best_pasta_shape: penne
  annotations:
    best_pizza_topping: basil
spec:
  containers:
  - name: hs-pizza-webapp-container
    image: ponderosa/hs-pizza-webapp:latest
    imagePullPolicy: Always
    ports:
    - containerPort: 1234
```

You can update the pod currently running in the cluster just by running `kubectl apply -f k8s/hs-pizza-webapp-pod.yaml`.

Although we haven't done so here, it's customary to include a prefix on annotations' key value to avoid collisions.[^4]

## Exercise: creating a pod for the topping-combo-service

Now that you've created a pod for the webapp service, you have the skills you need to create a pod for the topping combo service. Don't worry about how the pods will communicate with each other yet — we'll cover that in the next section. Here's what to do:

* create a pod manifest for the topping suggestion service at `k8s/hs-pizza-topping-suggestion-service-pod.yaml`. The pod should run the the `ponderosa/hs-pizza-topping-suggestion:latest` Docker image and specify `containerPort: 5678` (if you pushed up your own topping suggestion service Docker image to DockerHub in [the containerization module]({{ site.baseurl }}/02-containerization), feel free to use that image instead of the `ponderosa` one).
* Run the pod in your cluster.
* Use `kubectl port-forward yourpodname localPort:containerPort` to forward local traffic to your pod.
* Curl the `/topping_combo` endpoint to make sure everything's working.
* View the pod's logs using `kubectl logs`.
* Kill your pod.


[^1]: Port forwarding is a magical and awesome thing, but it's beyond the scope of this lab; you can read more [here](https://en.wikipedia.org/wiki/Port_forwarding).
[^2]: Note: `kubectl edit` isn't a  maintainable workflow, as your running workloads will drift from what's specified in your YAML. Generally if your pod's configuration is busted, it's good practice to delete it, update the YAML that generated it, and create an entirely new pod with `kubectl create -f`.
[^3]: Wondering what a TTY is? It's a teletypewriter and it's both important to accessibility _and_ an awesome bit of computing history. See: https://askubuntu.com/a/481919
[^4]: As an example: imagine an engineer working on the same cluster and decide to annotate one of their nodes with `active=true` for whatever reason. Then, they hook up some cluster automation software that _also_ tries to label that node with `active=true`. The annotation would error out! This could have been avoided if the application engineer had annotated the node with `mycoolcompany./active=true` and/or the automation software provider used the annotation `mycoolautomationcompany.rodeo/active=true`
