"""
  Flask App
"""
from src import create_app
from src.resources import initialize_resources
from src.utils.constant.response_messages import MESSAGE_WELCOME


app = create_app("flask.cfg")
initialize_resources(app)


@app.before_first_request
def log_health_message():
    """ Greets """
    print(MESSAGE_WELCOME)


if __name__ == "__main__":
    app.run()
