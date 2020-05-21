"""
  Flask App
"""
from flask_jwt_extended import JWTManager
from src import create_app
from src import db
from src.resources import initialize_resources

app = create_app("flask.cfg")


@app.before_first_request
def create_tables():
    """
       Initialize Database
    """
    db.init_app(app)
    db.create_all()


# no endpoint
jwt = JWTManager(app)


initialize_resources(app, jwt)

if __name__ == "__main__":
    app.run()
