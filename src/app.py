"""
  Flask App
"""
import os

from flask import request
from src import create_app
from src.resources import initialize_resources
from src.utils.constant.response_messages import MESSAGE_WELCOME
from src.utils.logger import info

app = create_app("flask.cfg")
initialize_resources(app)


@app.before_first_request
def log_health_message():
    """ Greets """
    info(MESSAGE_WELCOME)
    os.environ["API_HOST_URL"] = request.host_url


@app.before_request
def log_request_info():
    """ Request Interceptor """
    info("Request Path: {}".format(request.path))
    info("Request Headers:\n{}".format(str(request.headers).rstrip()))
    info("Request Body: {}".format(request.get_data().decode()))


# To-do Temporarily Adding static page url
@app.route("/reset-password")
def root():
    """ Loads static page """
    return app.send_static_file("reset-password.html")


if __name__ == "__main__":
    app.run()
