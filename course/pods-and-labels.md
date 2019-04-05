# Pods, Labels, and Annotations

Now that we've containerized HyprSk8l Pizza's services, it's time to move onto Kubernetes! In order to put a workload onto Kubernetes, we'll first need to have a Kubernetes installation, which is known as a "cluster" (a "cluster" because the installation is frequently on more than one machine). You can think of a cluster as an independent instance of Kubernetes. In the future, HyprSk8l's engineering organization may need several clusters, but for now, we'll just have one. 

HyprSk8l Pizza now has a working Kubernetes cluster! And a Docker container running its front-end web application! Now the question is … how do you get that Docker container running in the Kubernetes cluster? The answer? Pods.

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

### Creating a frontend service pod

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

To get our frontend service pod into Kubernetes, we first need to define a manifest. It'll look like this:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hs-pizza-frontend
spec:
  containers:
  - name: hs-pizza-frontend-container
    image: ponderosa/hs-pizza-frontend-service:0.1
    imagePullPolicy: Always
    ports:
    - containerPort: 1234
```

Create a file called `hs-pizza-frontend-pod.yaml` in the `k8s/` directory and paste in the above YAML.  Then, create it in the cluster by running `kubectl apply -f k8s/hs-pizza-frontend-pod.yaml`. Check and see what's up with `kubectl get pods`. Describe your running pod and see if you can figure out what's going on!

### Accessing your pod with port forwarding

Now that our Kubernetes pod is running, how do we get to it? Our Kubernetes cluster has security features that prevent anyone on the internet from accessing it without authentication, so we need to configure Kubernetes to serve traffic to your pod (that is...it has to get web requests somehow).  _For development purposes_, we can use the `kubectl port-forward` command to get traffic to its destination; in production, a high-security organization like HyperSk8l Pizza will use Kubernetes services to route traffic to pods (this will be covered a bit later in the lab.[^1]

Let's run `kubectl port-forward hs-pizza-frontend 5000:1234` to forward local traffic on port 5000 to port 1234 in the pod. Hit `http://localhost:5000/pod-info` and check out where your pod's running from!

Run `kubectl logs hs-pizza-frontend` to see the logs from the pod.

Once you're sufficiently wowwed, you can hit ctrl+c to stop port forwarding.

### Breaking, deleting, and relaunching a pod

`kubectl edit` is used to update API objects that already exist in the cluster. If you're not comfortable with `vim`, you may want to `export EDITOR=nano` before continuing.[^2] Let's edit our `hs-pizza-frontend` pod with `kubectl edit pod hs-pizza-frontend`. Update the YAML so that it points to a nonexistent image and save your changes (`:wq` in vim, if you're using that). Describe your pod again, and check out what happened to the pods in the cluster.

Once you're sufficiently satisfied that your pod is broken, delete your pod with `kubectl delete hs-pizza-frontend`.

### Executing commands inside a pod

`kubectl exec` is used to execute commands inside of a container, which lives inside of a pod. It can be used for one-off commands in the pod _or_ can be run in interactive TTY mode ( using the flags`-it`), which are commonly used to get a shell inside the pod and poke around its container(s).[^2] Getting an interactive shell inside of a container is often referred to as "shelling into a container."

Let's start by recreating our pod with `kubectl apply -f k8s/hs-pizza-frontend-pod.yaml`. We'll re-establish the port-forwarding with `kubectl port-forward hs-pizza-frontend 5000:1234`. Now, we'll check out the `/ls_tmp` endpoint, which lists the contents of the `/tmp` directory in the pod. Do that by running `curl localhost:5000/ls_tmp`.

Now, let's get inside of the pod by running `kubectl exec -it hs-pizza-frontend bash`. Make some files in the `/tmp` directory with `touch /tmp/whatever` and then `exit` to get out of the pod.

`curl` the `ls_tmp` endpoint again — you should see your file(s)!

### Adding labels and retrieving pods using selectors

In Kubernetes, you can mark objects in the cluster with arbitrary key/value pairs called [`labels`](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/). The command will look something like: `kubectl label object-type object-id labelkey=labelvalue` (a label is a key/value pair). Labels are incredibly useful when you want to deal with multiple Kubernetes objects as a logical unit, which is an essential feature for megascale web food delivery corporations like Hyprsk8l Pizza. 

You can show the labels attached to a given object by appending `--show-labels` to the `get` command. Labels will also appear if you `kubectl describe` an object. 

Let's start our labelling process by launching a second pod into the cluster. Run `kubectl apply -f resources/utility-pod.yaml` to launch a pre-defined pod. Next, run `kubectl get pods --show-labels` to show the different pods' labels. It's a travesty that `hs-pizza-frontend` doesn't have a `best-pasta-shape` label. We'll add one by running `kubectl label pod hs-pizza-frontend best-pasta-shape=penne`.

Instead of labeling pods by hand, it's often helpful to express labels in the pod manifest. First, delete the `hs-pizza-frontend` pod, then update its YAML to have the label defined:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hs-pizza-frontend
  labels:
    best_pasta_shape: penne
spec:
  containers:
  - name: hs-pizza-frontend-container
    image: ponderosa/hs-pizza-frontend-service:0.1
    imagePullPolicy: Always
    ports:
    - containerPort: 1234
```

Show the pods' labels using `kubectl get` again and make sure that the label was applied.

Next, we'll fetch pods by label selector. Let's get all the pods whose favorite pasta shape is rigatoni:
`kubectl get pods -l best_pasta_shape=rigatoni`.

### Adding annotation

Kubernetes supports another type of arbitrary key/value pairs: [annotations](https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/)! They *cannot be used to identify anything using the Kubernetes API* (you can't query on annotations in kubectl), but provide a way to tack information onto Kubernetes objects. Annotation are useful for third-party tooling, beta features, and more. When creating an annotation, it's customary to include a prefix on the key to avoid collisions.[^4]

Let's apply the completely ludicrous annotation `best_pizza_topping=ham` to one of our nodes. `kubectl annotate node minikube best_pizza_topping=ham`. Let's add a `best_pizza_topping` annotation to the pod manifest:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hs-pizza-frontend
  labels:
    best_pasta_shape: penne
  annotation:
  	best_pizza_topping: chocolate
spec:
  containers:
  - name: hs-pizza-frontend-container
    image: ponderosa/hs-pizza-frontend-service:0.1
    imagePullPolicy: Always
    ports:
    - containerPort: 1234
```

You can update the pod currently running in the cluster just by running `kubectl apply -f k8s/hs-pizza-frontend-pod.yaml`.

## Exercise: creating a pod for the topping-combo-service

Now that you've created a pod for the frontend service:

* create a pod template for the topping-suggestion-service at `k8s/topping-suggestion-service-pod.yaml`. The pod should run the the `ponderosa/hs-pizza-topping-suggestion-service:0.1` Docker image and specify `containerPort: 5678`.
* Run the pod in your cluster.
* Use `kubectl port-forward yourpodname localPort:containerPort` to forward local traffic to your pod.
* Curl the `/topping_combo` endpoint to make sure everything's working.
* View the pod's logs using `kubectl logs`.
* Kill your pod.


[^1]: Port forwarding is a magical and awesome thing, but it's beyond the scope of this lab; you can read more [here](https://en.wikipedia.org/wiki/Port_forwarding).
[^2]: Note: `kubectl edit` isn't a  maintainable workflow, as your running workloads will drift from what's specified in your YAML. Generally if your pod's configuration is busted, it's good practice to delete it, update the YAML that generated it, and create an entirely new pod with `kubectl create -f`.
[^3]: Wondering what a TTY is? It's a teletypewriter and it's both important to accessibility _and_ an awesome bit of computing history. See: https://askubuntu.com/a/481919
[^4]: As an example: imagine an engineer working on the same cluster and decide to annotate one of their nodes with `active=true` for whatever reason. Then, they hook up some cluster automation software that _also_ tries to label that node with `active=true`. The annotation would error out! This could have been avoided if the application engineer had annotated the node with `mycoolcompany./active=true` and/or the automation software provider used the annotation `mycoolautomationcompany.rodeo/active=true`
