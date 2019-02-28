# Lab 0 - Introducing Docker

## Introduction[^0]

HyprSk8l Pizza has decided to take their application onto Kubernetes, which means that they first need to **containerize** their application. Docker is a popular containerization technology, and Docker **containers** are typically what Kubernetes deploys. In this lab, we'll create a Docker **image** and make a running container based on that image. You can build Docker images on your local machine with the [docker build](https://docs.docker.com/engine/reference/commandline/build/) command. You can run them with the [docker run](https://docs.docker.com/engine/reference/run/) command.

The `frontend-python` directory contains a `Dockerfile` that's set up to run a webserver when a container based on this image is run.

## Exercise 0 - Build a Docker image

**Tasks:**

0. Build a Docker image on your machine using the `Dockerfile` in the `frontend-python` directory, making sure to tag it with `hs-pizza-frontend:1.0`.

**Useful docs:** [`docker build`](https://docs.docker.com/engine/reference/commandline/build/), [tag an image](https://docs.docker.com/engine/reference/commandline/build/#tag-an-image--t)

**Check your work**: run `docker images` and make sure that you have a `hs-pizza-frontend:1.0` image.

## Exercise 1 — Run a Docker container

**Tasks:**

0. Run the `hs-pizza-frontend:1.0` image on your local machine using the `docker run` command so that the in-container webserver's port (configured to be port 5000 in the last line of the `Dockerfile`) is available on your local machine's port 4000 (hint: check out the `-p` flag). 

**Useful docs:** [`docker run`](https://docs.docker.com/engine/reference/run/)

**Check your work**: When complete, you should be able to visit [http://localhost:4000](http://localhost:4000) in your browser and have your request served by the webserver running inside the container. `curl localhost:4000/pizza` should return something exciting.

## Exercise 2 — Kill a Docker container

**Tasks:**

0. use `docker ps` to find the running container and issue a `docker kill` command to kill it.

**Useful docs:** [`docker ps`](https://docs.docker.com/engine/reference/commandline/ps/), [`docker kill`](https://docs.docker.com/engine/reference/commandline/kill/)

**Check your work:** `docker ps | grep pizza` should return nothing.

## Exercise 3 — Create a new version of an existing Docker image

**Tasks:**

0. update the `pizza` method in `frontend-python` to return the 🆒 emoji. Rebuild the Docker image and tag it with `hs-pizza-frontend:1.1` (note the version bump).
1. Start the new image with `docker run`, bound to port 5555 (this should look pretty similar to the command you ran in exercise 1).

**Check your work**: `curl localhost:5555/pizza` should return the `cool` emoji.

## Exercise 4 — Push your Docker image to a container registry

**Task:** 

0. Tag your image with `yourdockerhubusername/hs-pizza-frontend:1.1`
1. Push your image to to [DockerHub](https://hub.docker.com/), making sure it's set to public.

**Useful docs:** [`docker login`](https://docs.docker.com/engine/reference/commandline/login/), [`docker push`](https://docs.docker.com/engine/reference/commandline/push/).

**Check your work**: Ask someone you know to pull down your Docker image: `docker pull yourdockerhubusername/hs-pizza-frontend:1.1`.

[^0]: If you are not currently in a [Ponderosa](https://ponderosa.io) class, you may want to read the [labs introduction](#todo) first.