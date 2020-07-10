"""
  Flask App
"""
from src import create_app
from src.resources import initialize_resources


app = create_app("flask.cfg")
initialize_resources(app)


@app.before_first_request
def log_health_message():
    """ Greets """
    print("Welcome to ap-auth-service")


if __name__ == "__main__":
    app.run()
