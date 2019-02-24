import os
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def hello():
    env = {}
    for env_var in os.environ.keys():
        env[env_var] = os.environ[env_var]
    hostname = env["HOSTNAME"]
    return render_template("index.html", env=env, hostname=hostname)


@app.route("/pod_info")
def pod_info():
    hostname = os.environ["HOSTNAME"]
    return_string = (f"Greetings from {hostname}!\n"
                     f"Access this pod with kubectl exec -it {hostname}\n"
                     f"Get logs with kubectl logs {hostname}\n"
                     "Get a slice of pizza at /pizza\n")
    return return_string


@app.route("/pizza")
def pizza():
    return "🍕🍕\n🥤\n🎉🎉🎉🎉🎉\n"
