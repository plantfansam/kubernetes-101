import json
import os

from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route("/")
def root():
    env = {}
    for env_var in os.environ.keys():
        env[env_var] = os.environ[env_var]
    hostname = env.get("HOSTNAME", "unknown")
    topping_suggestion_status = get_endpoint_health(
        topping_suggestion_health_check_endpoint(),
        "topping-suggestion service")
    frontend_status = get_endpoint_health(frontend_health_check_endpoint(),
                                          "webapp service")
    return render_template(
        "index.html",
        env=env,
        hostname=hostname,
        health_checks=[topping_suggestion_status, frontend_status])


def topping_suggestion_health_check_endpoint():
    return os.path.join(topping_suggestion_root_url(), "health-check")


def frontend_health_check_endpoint():
    return os.path.join(frontend_root_url(), "health-check")


def topping_suggestion_root_url():
    return os.environ.get("TOPPING_SUGGESTION_URL")


def frontend_root_url():
    return os.environ.get("WEBAPP_URL")


def css_class_for_status(status):
    if status == 200:
        return "has-background-success"
    else:
        return "has-background-danger"


def get_endpoint_health(health_check_endpoint, label):
    try:
        request = requests.get(health_check_endpoint, timeout=1)
        healthy = request.status_code == 200
        status_code = request.status_code
    except requests.exceptions.RequestException:
        healthy = False
        status_code = None
    css_class = css_class_for_status(status_code)
    return {
        "label": label,
        "endpoint": health_check_endpoint,
        "status_code": status_code,
        "healthy": healthy,
        "css_class": css_class
    }