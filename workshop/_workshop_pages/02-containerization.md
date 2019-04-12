---
layout: workshop-page
title: "Containerization"
---

HyprSk8l Pizza has decided to take their application onto Kubernetes, which means that we first need to **containerize** our application. Docker is a popular [containerization](https://en.wikipedia.org/wiki/Container_(virtualization)) technology, and Docker **containers** are typically what Kubernetes deploys. In this section, we'll prepare our app for deployment on Kubernetes by containerizing our frontend service and our topping suggestion service. 

> If you'd like more in-depth background on the topics covered here, check out our [video course](UDEMY_URL)
{: class="video-plug"}

## Containerizing our Services

### Writing the frontend-service Dockerfile

HyprSk8l Pizza needs to leverage the power of Docker images to put the app on Kubernetes, and the first step to making a Docker **image** is defining that image with a file called a **Dockerfile**.

Let's start by writing a Dockerfile for the frontend service — we'll create a file called `Dockerfile` in the `frontend-service` directory: 

```Dockerfile
FROM python:3.7.2-stretch

ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app

ENV FLASK_APP=app.py
CMD ["flask", "run", "-p", "1234", "-h", "0.0.0.0"]
```

The Docker image created by this Dockerfile has everything the app needs to run. The final line contains the default command, which is run whenever you create a Docker container based on this Docker image. You'll notice that we are serving the application on port `1234` and binding to the host `0.0.0.0`.

### Building the frontend service Docker image

Writing a Dockerfile doesn't give you a Docker image. To get a Docker image from a Dockerfile, you must **build** (some call it "baking") a Docker image using the [docker build](https://docs.docker.com/engine/reference/commandline/build/) command (you could also use a tool like [`buildah`](https://buildah.io/), but we won't).

From within the `frontend-service` directory, run `docker build -t yourname/hs-pizza-frontend-service:0.1 .`. This creates your Docker image.

The `-t` flag is there to **tag** our Docker image so we can easily refer to it in the future — I'd recommend changing it to have your name as a prefix.

### Running the frontend service Docker image

Now that we have the Docker image, let's put it to use by running it. When you run a Docker image, you create a **container**, which is a running process (I like to think of Docker containers as Docker images in italics).

From anywhere on your machine, run `docker run -p 9999:1234 yourname/hs-pizza-frontend-service:0.1` (the `-p` flag says to forward traffic from port `9999` on our host machine to port `1234` inside the Docker container). Now, visit `localhost:9999`. You should see a slightly broken HyprSk8l Pizza homepage. The topping-combo-suggester service is not available!

### Killing the frontend service Docker container

To kill your running Docker container, we'll use the `docker ps` and `docker kill` commands. Open up a new tab in your terminal and run `docker ps` — you should see your running container. Run `docker kill asdfghjkl`, where `asdfghjl` is the `CONTAINER ID` in the leftmost column of the `docker ps` output.

### Pushing the Docker image to a registry

Once we're confident that our Docker image works, we can push it to a Docker registry, so it's easily downloadable. A Docker registry lets you (and others that are granted access) retrieve baked Docker images so they can be run on different machines (which is the whole point!). We'll be using DockerHub, which offers both public and private Docker image repositories — for ease of retrieval, we'll use public ones, but production applications should use private repositories.

> It's possible to use Ponderosa's pre-baked images for the rest of the tutorial, so feel free to skip to the next section if you aren't interested.
{: class=skippable }

To push our image, we need to [register for a DockerHub account](https://hub.docker.com/signup), and note your Docker ID. Once registered, run `docker login` to authenticate against DockerHub.

Next, run `docker images` and look for the image we just baked (you might want to run `docker images | grep frontend`). When you find it, we'll re-tag our image if necessary — the tag should be in the format `yourDockerID/frontend-service:0.1`. You can re-tag by noting the `IMAGE ID` and running `docker tag IMAGE_ID yourDockerID/frontend-service:0.1`.

Once you have tagged the image, just run `docker push yourDockerID/frontend-service:0.1`. The argument to the `docker push` command is just the name of the tag on your host.

## Exercise: creating, running, and pushing the topping suggestion service image

For this exercise, use the following Dockerfile to create a Docker image for the topping suggestion service, which is in the `topping-suggestion-service` directory. We'll use the tag `yourname/hs-pizza-topping-suggestion-service:0.1`.

```Dockerfile
FROM python:3.7.2-stretch

ADD requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app

ENV FLASK_APP=app.py

# Notice that the Flask app is configured to serve on port `5678`.
CMD ["flask", "run", "-p", "5678", "-h", "0.0.0.0"]
```

Once you have created your Docker image, run a container based on that image and hit the `/topping_combo` endpoint to verify it's working. Finally, push the image to DockerHub.

**Useful docs**: [`docker build`](https://docs.docker.com/engine/reference/commandline/build/), [tag an image](https://docs.docker.com/engine/reference/commandline/build/#tag-an-image--t), [`docker run`](https://docs.docker.com/engine/reference/run/), [`docker kill`](https://docs.docker.com/engine/reference/commandline/kill/), [`docker login`](https://docs.docker.com/engine/reference/commandline/login/), [`docker push`](https://docs.docker.com/engine/reference/commandline/push/).