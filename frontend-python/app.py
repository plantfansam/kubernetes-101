import os
import requests
from flask import Flask, render_template
app = Flask(__name__)


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
        "index.html", topping_combo=topping_combo, errors=errors)


@app.route("/pizza")
def pizza():
    return "🍕🍕\n🥤\n🎉🎉🎉🎉🎉\n"


def get_topping_combo_from_microservice():
    topping_combo_endpoint = os.path.join(topping_combo_suggester_root_url(),
                                          "topping_combo")
    return requests.get(topping_combo_endpoint, timeout=1)


def topping_combo_suggester_root_url():
    return os.environ.get("TOPPING_COMBO_SUGGESTER_URL",
                          "https://www.google.com")
