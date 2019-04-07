# Introduction

Welcome to Kubernetes 101! In this workshop we'll take Silicon Valey's latest darling, HyprSk8l Pizza, and put its flagship, AI-powered Pizza Topping Suggestion web app on Kubernetes. When healthy, the website looks like  this:

![Application screenshot](./application-screenshot.png)

On every web request, you get a new pizza topping combo suggestion:

![main-app-demo.gif](./main-app-demo.gif)

How does this amazing application work? Funny you should ask...before putting an application on Kubernetes, it's necessary to understand its functions and architecture.

## The application's architecture

The application is composed of two services:

1. The **frontend service**, which takes web requests from users and renders a response after making a call to the **topping suggestion service** to retrieve a new pizza topping combination.
2. The **topping suggestion service**, which returns topping combination suggestions from the `topping_combo` endpoint.

Here's an admittedly crude service diagram:

![Service Diagram](./service-diagram.jpg)

## The GitHub repository

The GitHub repository is laid out as follows:

* `/workshop` — contains Markdown documents guiding participants through the workshop
* `/frontend-service` — contains a Flask app that runs the frontend service
* `/topping-suggestion-service` — contains a Flask app that runs the topping suggestion service
* `/resources` — contains files used in the workshop
* `/k8s` — an empty directory that we suggest putting Kubernetes manifests in (this is just a suggestion and is not required by Kubernetes).

### How to run the applications

Both the frontend service and the topping suggestion service are [Flask](http://flask.pocoo.org/) apps — Flask is a dead simple Python web framework, which was chosen for its ease of use and understanding (as long as you know a programming language, I promise you can figure Flask out in less than 5 minutes).

To run either application, navigate to its directory and run `flask run -p 1234`, where `1234` is the port on `localhost` you want to serve the application on.

Note: the frontend service expects a `COMBO_SUGGESTER_URL` environment variable pointing to a working instance of the topping suggestion service. So if topping suggestion service is running on localhost:2222, you would want to run `COMBO_SUGGESTER_URL=http://localhost:2222 flask app`.

## Workshop outline

* [01-introduction](#)
* [02-containerization](02-containerization.md)
* [03-clusters](03-clusters.md)
* [04-pods-and-labels](04-pods-and-labels.md)
* [05-services](05-services.md)
* [06-replicasets](06-replicasets.md)
* [07-deployments](07-deployments.md)
* [08-configmaps](08-configmaps.md)
* [09-secrets](09-secrets.md)
* [10-volumes](10-volumes.md)
* [11-statefulsets](11-statefulsets.md)
* [12-jobs](12-jobs.md)
* [13-resources](13-resources.md)