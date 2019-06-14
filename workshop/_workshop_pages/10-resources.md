---
layout: workshop-page
title: "Resource requests and limits in Kubernetes"
---

After moving itopping suggestion servicelication to Kubernetes, HyperScale Pizza is seeing sporadic performance issues. Some investigation reveals that these issues are correlated with the `/extremely-expensive-operation` endpoint in the `topping-suggestion-service` application. It turns out that when this endpoint is hit, the pod running the application starts hogging RAM to the point that other requests are slowed down. Shocking! I can't believe it was that endpoint...

## Limiting resource usage

When run on a traditional server, applications are bound by the resource limitations of their host — they can only use as much CPU and RAM as is available on the box — and Kubernetes pods have the same constraints. The difference, however, is that Kubernetes is designed to run multiple pods on the same server. All of a sudden, the pod can't expect to use all of the host's resources, since other pods may also need those resources.

For this reason, it is extremely advisable to set resource requests and resource limits for both memory and CPU. Resource requests and resource limits are set on the container level (not the pod level).

### Resource requests vs resource limits

Resource _requests_ are used to place a pod on a node that has adequate resources to run it. When you tell Kubernetes to run a pod that needs X amount of CPU and X amount of memory, it finds a node that has adequate available resources to run it on, then places it there (see more details [here](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/#how-pods-with-resource-requests-are-scheduled)).

Resource _limits_ are used to cut a pod off when it starts hogging resources. In the case when CPU exceeds the specified limit, CPU access is simply throttled (which slows down whatever operation is happening). When memory use exceeds the specified limit, it is eligible to be restarted.

When you're just getting started, it can be easier to set resource requests and resource limits to the same value.

## Setting resource limits

With this knowledge about resource requests and limits in hand, let's take a look at the `/extremely-expensive-operation` endpoint. What's it doing that uses so much memory? Checking it out in the browser starts to give a clue:

![extremely expensive endpoint: 2 raised to an arbitrary power](./extremely-expensive-endpoint.png)

It looks like the team shipped a killer feature where we raise 2 to an arbitrary power...that can use quite a lot of RAM! The code raises 2 to the power of whatever's set in `?pizza_exponent=`:

```
@app.route("/extremely-expensive-operation")
def extremely_expensive_operation():
    exponent = int(request.args.get("pizza_exponent")) or 0
    return f"2 raised to the power of {exponent} gives you ... {2**exponent} pizzas. That's a lot of pizza."
``` 

Checking the logs, we can see that people are throwing some extremely large numbers at us...

```
[17/May/2019 14:02:22] "GET /extremely-expensive-operation?pizza_exponent=3 HTTP/1.1" 200 -
[17/May/2019 14:02:25] "GET /extremely-expensive-operation?pizza_exponent=8000000000 HTTP/1.1" 200 -
[17/May/2019 14:02:25] "GET /extremely-expensive-operation?pizza_exponent=4000000000 HTTP/1.1" 200 -
```

This explains a lot! Our application is raising two to the eight billionth power — that uses a lot of memory! Let's set a RAM resource limit on our application so that this type of request doesn't affect other pods running on the node. Let's update `k8s/frontend-service-deployment.yaml` to include a memory request and memory limit of `1Gi`:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-service-deployment
  labels:
    app: hs-pizza-webapp
    workshop: kubernetes-101
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
  selector:
    matchLabels:
      app: hs-pizza-webapp
      workshop: kubernetes-101
  template:
    metadata:
      labels:
        app: hs-pizza-webapp
        workshop: kubernetes-101
    spec:
      containers:
      - name: hs-pizza-webapp-container
        image: ponderosa/hs-pizza-webapp:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 1234
        readinessProbe:
          httpGet:
            path: /health-check
            port: 1234
        env:
          - name: SHOW_PIZZA
            valueFrom:
              configMapKeyRef:
                name: webapp-configmap
                key: SHOW_PIZZA
          - name: SECRET_PIZZA_PASSWORD
            valueFrom:
              secretKeyRef:
                name: webapp 
                key: SECRET_PIZZA_PASSWORD
        resources:
          requests:
            memory: "1Gi"
          limits:
            memory: "1Gi"
```

Let's apply it to the cluster with `kubectl apply -f k8s/frontend-deployment.yaml`.