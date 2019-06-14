---
layout: workshop-page
title: "Kubernetes Jobs"
---

## What are Kubernetes Jobs and why might you use them?

While web applications like HyperScale Pizza typically need to run 24/7/365, other software is designed to run a fixed set of operations to completion. Think of data processing workloads, database migrations, data exports, etc. Kubernetes offers a first-class way of running these workloads: the job. In a job specification, you declare a container image, a command to run inside that container image, and a few other parameters (such as how many times the job should retry if it fails).

## Creating a Kubernetes job

HyperScale Pizza is working on a killer feature in which a job logs out a topping suggestion surrounded by a bunch of pizza emojis (despite the fact that logs are only visible to engineers, customers are clambering for it!). The code for the job has already been written and can be viewed at `topping-suggesion/jobs/log_out_pizza_emojis.py`; it can be invoked with `python topping-suggestion-service/jobs/log_out_pizza_emojis.py`. All that's left is to deploy it on Kubernetes.

Let's create a Kubernetes job to run this Python script. The manifest will look like this:

```
apiVersion: batch/v1
kind: Job
metadata:
  name: hs-pizza-log-out-pizza-emoji-job
spec:
  template:
    spec:
      containers:
      - name: topping-combo-suggestion
        image: ponderosa/hs-pizza-topping-suggestion:latest 
        command: ["python", "jobs/log_out_pizza_emojis.py"]
      restartPolicy: Never
  backoffLimit: 0
```

We're telling Kubernetes that we want to run `python jobs/log_out_pizza_emojis.py` inside of the `ponderosa/hs-pizza-topping-suggestion:latest` Docker image. The innermost `spec` here defines the pod in which our command will run, just like in a replicaSet.

Save this manifest in `k8s/emoji-job.yaml` and run `kubectl apply -f k8s/emoji-job.yaml`. You'll see something like this:

```
$ kubectl apply -f k8s/emoji-job.yaml
job.batch/hs-pizza-log-out-pizza-emoji-job created
```

If you run `kubectl get pods | grep pizza-emoji-job`, you'll see something interesting: a pod that looks like it was created by our job:

```
$ kubectl get pods | grep pizza-emoji-job
hs-pizza-log-out-pizza-emoji-job-q6zks           0/1     Completed   0          100s
```

This is because a job doesn't do any work itself — it launches _pods_ to do work for them. So to view the output of our job, we can get the logs of that pod with `kubectl logs hs-pizza-log-out-pizza-emoji-job-q6zks`:

```
🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕

       zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz  aaaaaaaaaaaaa
       z:::::::::::::::zz:::::::::::::::z  a::::::::::::a
       z::::::::::::::z z::::::::::::::z   aaaaaaaaa:::::a
       zzzzzzzz::::::z  zzzzzzzz::::::z             a::::a
             z::::::z         z::::::z       aaaaaaa:::::a
            z::::::z         z::::::z      aa::::::::::::a
           z::::::z         z::::::z      a::::aaaa::::::a
          z::::::z         z::::::z      a::::a    a:::::a
         z::::::zzzzzzzz  z::::::zzzzzzzza::::a    a:::::a
        z::::::::::::::z z::::::::::::::za:::::aaaa::::::a
       z:::::::::::::::zz:::::::::::::::z a::::::::::aa:::a
       zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz  aaaaaaaaaa  aaaa


🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕
```

Now that's what I call a feature!

## Parallelism and completions

Kubernetes jobs keep track of how many _completions_ they have — by default a job expects to be completed successfully once, and a _completion_ is recorded when a pod launched by a job exits with a `0` status code.

You can also configure a job to run to completion more than once, and control how many copies of that job can be run simultaneously (a parameter known as `parallelism`).

Let's configure our job to run 20 times and allow 5 pods to run at any given time:

```
apiVersion: batch/v1
kind: Job
metadata:
  name: hs-pizza-log-out-pizza-emoji-job-parallel
spec:
  template:
    spec:
      containers:
      - name: topping-combo-suggestion
        image: ponderosa/hs-pizza-topping-suggestion:latest 
        command: ["python", "jobs/log_out_pizza_emojis.py"]
      restartPolicy: Never
  backoffLimit: 0
  completions: 20
  parallelism: 5
```

Save this manifest in `k8s/emoji-parallel-job.yaml` and apply it to the cluster with `kubectl apply -f k8s/emoji-parallel-job.yaml`. You should see a whole lot of pods spawned by this job!

```
$ kubectl get pods | grep parall
hs-pizza-log-out-pizza-emoji-job-parallel-5lh4k   0/1     Completed   0          7s
hs-pizza-log-out-pizza-emoji-job-parallel-7ltmd   0/1     Completed   0          11s
hs-pizza-log-out-pizza-emoji-job-parallel-7xs9r   0/1     Completed   0          8s
hs-pizza-log-out-pizza-emoji-job-parallel-8dwvs   0/1     Completed   0          9s
hs-pizza-log-out-pizza-emoji-job-parallel-d2drg   0/1     Completed   0          7s
hs-pizza-log-out-pizza-emoji-job-parallel-d8w4m   0/1     Completed   0          8s
hs-pizza-log-out-pizza-emoji-job-parallel-dcbzn   0/1     Completed   0          9s
hs-pizza-log-out-pizza-emoji-job-parallel-dvgzb   0/1     Completed   0          14s
hs-pizza-log-out-pizza-emoji-job-parallel-jpg8q   0/1     Completed   0          14s
hs-pizza-log-out-pizza-emoji-job-parallel-kr2tf   0/1     Completed   0          14s
hs-pizza-log-out-pizza-emoji-job-parallel-ltm75   0/1     Completed   0          14s
hs-pizza-log-out-pizza-emoji-job-parallel-nvqdg   0/1     Completed   0          12s
hs-pizza-log-out-pizza-emoji-job-parallel-pg24b   0/1     Completed   0          11s
hs-pizza-log-out-pizza-emoji-job-parallel-qzn7b   0/1     Completed   0          7s
hs-pizza-log-out-pizza-emoji-job-parallel-qzsxp   0/1     Completed   0          14s
hs-pizza-log-out-pizza-emoji-job-parallel-rb524   0/1     Completed   0          10s
hs-pizza-log-out-pizza-emoji-job-parallel-vdcbc   0/1     Completed   0          13s
hs-pizza-log-out-pizza-emoji-job-parallel-vzt9b   0/1     Completed   0          9s
hs-pizza-log-out-pizza-emoji-job-parallel-w9n5d   0/1     Completed   0          10s
hs-pizza-log-out-pizza-emoji-job-parallel-wbkcb   0/1     Completed   0          11s
```

You can also see that the job itself has registered the number of successful completions:

```
$  kubectl get jobs | grep parallel
hs-pizza-log-out-pizza-emoji-job-parallel   20/20         10s        17h
```

## Backoff limits

Like even the best software engineers and DevOps professionals, jobs sometimes fail. The Kubernetes `job` resource allows you to specify how many times the job should attempt to run before giving up altogether. Let's create a new job template at `k8s/failing-job.yaml` that looks like this:

```
apiVersion: batch/v1
kind: Job
metadata:
  name: hs-pizza-failing-job
spec:
  template:
    spec:
      containers:
      - name: topping-combo-suggestion
        image: ponderosa/hs-pizza-topping-suggestion:latest 
        command: ["/bin/bash", "-c", "echo 'exiting with error' && exit 1"]
      restartPolicy: Never
  backoffLimit: 0
```

Here, we're telling the pod to run a simple bash script: `echo 'exiting with error && exit 1`. The nonzero [exit code](https://en.wikipedia.org/wiki/Exit_status) tells Kubernetes that the command failed — other more complex scripts will also exit with nonzero statuses if there is a problem. We're also setting the `backoffLimit` at `0`, indicating that we do not want the job to try to rerun this pod if it fails. The output from `kubectl get jobs` indicates that the job has not run to completion:

```
kubectl get jobs
NAME                                        COMPLETIONS   DURATION   AGE
hs-pizza-failing-job                        0/1           4m7s       4m7s
```

We can see that there is only one pod launched by the pod, and that it has an `Error` state:

```
$ kubectl get pods | grep failing
hs-pizza-failing-job-klfbg                        0/1     Error       0          4m26s
```

Let's delete the existing job with `kubectl delete job hs-pizza-failing-job` and bump up the `backoffLimit` so that the job manifest looks like this:

```
apiVersion: batch/v1
kind: Job
metadata:
  name: hs-pizza-failing-job
spec:
  template:
    spec:
      containers:
      - name: topping-combo-suggestion
        image: ponderosa/hs-pizza-topping-suggestion:latest 
        command: ["/bin/bash", "-c", "echo 'exiting with error' && exit 1"]
      restartPolicy: Never
  backoffLimit: 3
```

Apply the configuration to the cluster with `kubectl apply -f k8s/failing-job.yaml` and run `kubectl get pod | grep failing`. You should see the job re-trying by creating new pods over time:

```
get pod | grep failing
hs-pizza-failing-job-4qpks                        0/1     Error       0          5s
hs-pizza-failing-job-7pm6w                        0/1     Error       0          17s
hs-pizza-failing-job-dsws5                        0/1     Error       0          15s
```

If you inspect the logs of any of them, you can see that the pod indeed ran:

```
$ kubectl logs -f hs-pizza-failing-job-4qpks
exiting with errror
```

## Cleaning up jobs

If you've followed along in the terminal so far, you likely have a lot of cruft hanging around your cluster. `kubectl get jobs` probably returns quite a few different jobs:

```
$ kubectl get jobs
hs-pizza-failing-job                        0/1           7m         7m
hs-pizza-log-out-pizza-emoji-job            1/1           1s         18h
hs-pizza-log-out-pizza-emoji-job-parallel   20/20         10s        17h
```

Similarly, there are probably a lot of completed or errored pods hanging around (too many to include on this page, in fact..., but run `kubectl get pods | grep job`) to get an idea.

This can be really useful if you want to debug issues with jobs – since pods' logs disappear when the pods are deleted — but also makes the cluster hard to navigate since there's so much junk. At the beginning of the module, we created a job called `hs-pizza-log-out-pizza-emoji-job`, which is still hanging around the cluster:

```
$ kubectl get job hs-pizza-log-out-pizza-emoji-job
NAME                               COMPLETIONS   DURATION   AGE
hs-pizza-log-out-pizza-emoji-job   1/1           1s         18h
```

The job's pod is also still around:

```
# Grep for the name of the job and exclude results which include the world 'parallel'
$ kubectl get pod | grep hs-pizza-log-out-pizza-emoji-job | grep -v parallel
hs-pizza-log-out-pizza-emoji-job-q6zks            0/1     Completed   0          18h
```

To get rid of the job and its pods, just run `kubectl delete job hs-pizza-log-out-pizza-emoji-job`.

```
$ kubectl delete job hs-pizza-log-out-pizza-emoji-job
job.batch "hs-pizza-log-out-pizza-emoji-job" deleted
```

Now, if we look for pods belonging to that job, they've also gone away:

```
$ kubectl get pod | grep hs-pizza-log-out-pizza-emoji-job | grep -v parallel
$ 
```

## Exercise: writing a job manifest

First, delete the remaining jobs in the cluster with `kubectl delete job --all`.

Once you've done that, write a job manifest that runs the script `jobs/log_out_meal.py`, which is present in the `ponderosa/hs-pizza-topping-suggestion:latest` Docker image. The script is invoked as follows:

`python jobs/log_out_meal.py lunch`
`python jobs/log_out_meal.py dinner`

Depending on the argument to the script (`lunch` or `dinner`), the script will display different meals. Feel free to create multiple job files to run different versions of the script.

When you've launched the jobs in your cluster, verify the output with `kubectl logs <pod-name>`.