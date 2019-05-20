import os
import sys
from types import SimpleNamespace

import requests
from flask import Flask, render_template, request
app = Flask(__name__)

SECRET_PIZZA_PASSWORD = "pizzarules"


@app.route("/")
def root():
    topping_combo_request = get_topping_combo_from_microservice()
    if topping_combo_request.status_code == 200:
        topping_combo = topping_combo_request.json()['description']
        errors = None
    else:
        topping_combo = None
        combo_error = f"""Received status {topping_combo_request.status_code}
                          from topping-combo-suggestion service.
                          Configured to use topping-combo-suggestion service url
                          {topping_combo_suggester_root_url()}.
                       """
        errors = [combo_error]
    return render_template(
        "index.html",
        topping_combo=topping_combo,
        errors=errors,
        show_pizza=os.environ.get("SHOW_PIZZA", False),
        show_secret_pizza=pizza_password_correct())


@app.route("/health-check")
def health_check():
    return "True"


@app.route("/pizza")
def pizza():
    return "🍕🍕\n🥤\n🎉🎉🎉🎉🎉\n"


@app.route("/pod_info")
def pod_info():
    pod_hostname = hostname()
    return_string = (f"Greetings from HOSTNAME {pod_hostname}!\n"
                     f"Access this pod with kubectl exec -it {pod_hostname}\n"
                     f"Get logs with kubectl logs {pod_hostname}\n"
                     "Get a slice of pizza at /pizza\n")
    return return_string


@app.route("/ls_tmp")
def ls_tmp():
    pod_hostname = hostname()
    listing = os.listdir("/tmp")
    return_string = (f"Listing files in /tmp on HOSTNAME {pod_hostname}:\n"
                     f"{listing}\n")
    return return_string


@app.route("/extremely-expensive-operation")
def extremely_expensive_operation():
    exponent = int(request.args.get("pizza_exponent") or 0)
    return f"2 raised to the power of {exponent} gives you ... {2**exponent} pizzas. That's a lot of pizza."


def hostname():
    return os.environ.get("HOSTNAME", "unknown")


def get_topping_combo_from_microservice():
    topping_combo_endpoint = os.path.join(topping_combo_suggester_root_url(),
                                          "topping_combo")
    try:
        return requests.get(topping_combo_endpoint, timeout=1)
    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
        return SimpleNamespace(**{"status_code": "????"})


def topping_combo_suggester_root_url():
    return os.environ.get("TOPPING_COMBO_SUGGESTER_URL",
                          "http://topping-suggestion-service")


def pizza_password_correct():
    return os.environ.get("SECRET_PIZZA_PASSWORD", "") == SECRET_PIZZA_PASSWORD
