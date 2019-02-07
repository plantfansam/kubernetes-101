# README for Frontend

This directory contains a front-end application that helps explore Kubernetes.

## Local Setup

Don't worry about setting the repository up locally unless you are updating this training. If you're doing that, you can run it locally with:

* `brew install yarn`
* `yarn install`
* `yarn start`

## Building Docker Images

The directory contains a `Dockerfile`, which is used for building a [Docker image](https://docs.docker.com/engine/reference/commandline/images/). To build this image, run `docker build -t kubernetes-101-frontend:1.0.` from this directory.

## Running the Docker Image as a Container

A Docker container is a running instance of a Docker image; it can be run anywhere that Docker is installed. To make it happen, run `docker run -p 8080:8080 kubernetes-101-frontend:1.0`. The `-p` flag binds the port on which the webserver is running (_inside_ the container) to the port on the host where Docker is running. 
