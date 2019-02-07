# Lab 0 - Introducing Docker

## Introduction

Docker is a popular containerization technology, and Docker containers are typically what Kubernetes deploys. In this lab, we'll create a Docker *image* and make a running *container* based on that image. You can build Docker _images_ on your local machine with the [docker build](https://docs.docker.com/engine/reference/commandline/build/) command. You can run them with the [docker run](https://docs.docker.com/engine/reference/run/) command.

The `frontend` directory contains a `Dockerfile` that's set up to run a webserver when a container based on this image is run.

## Exercise 0 - Build a Docker image

**Task:** using [`docker build`](https://docs.docker.com/engine/reference/commandline/build/), create a Docker image on your machine using the `Dockerfile` in the `frontend` directory. Tag it with `kubernetes-101-frontend:1.0`.

**Useful docs:** [`docker build`](https://docs.docker.com/engine/reference/commandline/build/)

**Check your work**: `docker images | grep kubernetes-101-frontend:1.0 | wc -l == 1`

## Exercise 1 — Run a Docker container

**Task:** run the `kubernetes-101-frontend:1.0` image on your local machine using the `docker run` command so that the in-container webserver's port (8080) is available on your local machine's port 4000 (hint: check out the `-p` flag). When complete, you should be able to visit [http://localhost:4000](http://localhost:4000) and have your request served by the webserver running inside the container.

**Useful docs:** [`docker run`](https://docs.docker.com/engine/reference/run/)

**Check your work**: `wget localhost:4000`.

## Exercise 2 — Kill a Docker container

**Task:** use `docker ps` to find the running container. Issue a `docker kill` command to kill it.

**Useful docs:** [`docker ps`](https://docs.docker.com/engine/reference/commandline/ps/), [`docker kill`](https://docs.docker.com/engine/reference/commandline/kill/)

**Check your work:** `docker ps | grep frontend | wc -l == 0` 

## Exercise 3 — Create a new version of an existing Docker image

**Task:** update the `h1` tag in `frontend/client/components/App.jsx` to read `<h1>Kubernetes 101</h1>` and then make a new version of the docker image at `kubernetes-101-frontend:1.1` (note the version bump). Then start the new image with `docker run` bound to port 4000.

**Check your work**: `wget localhost:4000 | grep '<h1>Kubernetes 101</h1>' | wc -l`

## Exercise 4 — Push your Docker image to a container registry

**Task:** tag your image with `yourdockerhubusername/kubernetes-101-frontend:1.1` and then push it to to [DockerHub](https://hub.docker.com/).

**Useful docs:** [`docker login`](https://docs.docker.com/engine/reference/commandline/login/), [`docker push`](https://docs.docker.com/engine/reference/commandline/push/).

**Check your work**: Ask your neighbor to pull down your Docker image: `docker pull yourdockerhubusername/kubernetes-101-frontend:0.1`.

