import functools
import os
import random
from flask import Flask, jsonify, render_template
app = Flask(__name__)

FOOD_DIRECTORY = "foods"


@app.route("/health-check")
def health_check():
    return "True"


@app.route("/topping_combo")
def topping_combo():
    all_toppings = get_toppings()
    topping_combo = random.sample(all_toppings, k=3)
    topping_string = to_sentence(topping_combo)
    return jsonify({
        'toppings': topping_combo,
        'description': f"Please enjoy this {topping_string} pizza!"
    })


@functools.lru_cache()
def get_toppings():
    toppings = []

    for topping_list in os.listdir(FOOD_DIRECTORY):
        topping_file = open(os.path.join(FOOD_DIRECTORY, topping_list))
        [toppings.append(topping[:-1]) for topping in topping_file]
        topping_file.close()

    return toppings


def to_sentence(topping_list):
    return_string = ""
    if os.environ.get("TOPPING_MODE", "").upper() == "SPICY":
        return_string += "🌶️🌶️🌶️ WILDLY SPICY "

    for index, topping in enumerate(topping_list):
        if index == len(topping_list) - 1:
            return_string += f"and {topping}"
        else:
            return_string += f"{topping}, "

    return return_string