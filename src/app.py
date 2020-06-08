"""
  Flask App
"""
from sqlalchemy.exc import OperationalError
from src import create_app
from src import db
from src import redis_instance
from src.resources import initialize_resources


app = create_app("flask.cfg")


@app.before_first_request
def create_tables():
    """
       Initialize Database
    """
    try:
        db.init_app(app)
        db.create_all()
    except OperationalError:
        pass


initialize_resources(app, redis_instance)

if __name__ == "__main__":
    app.run()
