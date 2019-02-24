import os
import requests
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def root():
    topping_combo = get_topping_combo_from_microservice()
    return render_template("index.html", topping_combo=topping_combo)


@app.route("/pizza")
def pizza():
    return "🍕🍕\n🥤\n🎉🎉🎉🎉🎉\n"


def get_topping_combo_from_microservice():
    topping_combo_endpoint = os.path.join(
        os.environ["TOPPING_COMBO_SUGGESTER_URL"], "topping_combo")
    request = requests.get(topping_combo_endpoint, timeout=3)
    return request.json()['description']