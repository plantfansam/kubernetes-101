# README

This directory contains the webapp service. This service is responsible for fielding HTTP requests from the public internet and rendering a response to the user. The webapp service makes a call to the topping combo suggestion service, so it expects an environment variable called TOPPING_COMBO_SUGGESTION_SERVICE_URL which points to a running version of that service.

## Running the application 

First, make sure you have `pip` by running `which pip` (`pip` is a python package manager, and this application uses python packages). 

Next, install requirements by running `pip install -r requirements.txt` from this directory.

Finally, run `flask run -p 1234 -h 0.0.0.0` from this directory to run the application on port `1234`.

Note: the webapp service expects a `TOPPING_COMBO_SUGGESTION_SERVICE_URL` environment variable pointing to a working instance of the topping suggestion service. So if topping suggestion service is running on `localhost:2222`, you would want to run `TOPPING_COMBO_SUGGESTION_SERVICE_URL=http://localhost:2222 flask run -p 1234 -h 0.0.0.0`.