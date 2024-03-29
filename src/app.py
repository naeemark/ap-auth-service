"""
  Flask App
"""
from flask import request
from src import create_app
from src.resources import initialize_resources
from src.utils.constant.response_messages import MESSAGE_WELCOME
from src.utils.logger import log_info
from src.utils.utils import log_request_info

app = create_app("flask.cfg")
initialize_resources(app)


@app.before_first_request
def log_health_message():
    """ Greets """
    log_info(MESSAGE_WELCOME)


@app.before_request
def log_request():
    """ Request Interceptor """
    log_request_info(request)


# To-do Temporarily Adding static page url
@app.route("/api/reset-password")
def root():
    """ Loads static page """
    return app.send_static_file("reset-password.html")


if __name__ == "__main__":
    app.run()
