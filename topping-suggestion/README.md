# README

This directory contains the topping suggestion service. The topping suggestion service is not hit directly by users - the webapp service hits the `/topping_combo` endpoint, which returns JSON that contains a delectable combination of pizza toppings (e.g. basil, thyme, and quail).

## Running the application 

First, make sure you have `pip` by running `which pip` (`pip` is a python package manager, and this application uses python packages).

Next, install requirements by running `pip install -r requirements.txt` from this directory.

Finally, run `flask run -p 5678 -h 0.0.0.0` from this directory to run the application on port `5678`.
