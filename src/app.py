"""
  Flask App
"""
from flask_jwt_extended import JWTManager
from src import create_app
from src import db
from src.resources import initialize_resources
from src.resources import initialize_token_in_blacklist_loader
from src.resources import redis_instance
from src.utils.blacklist_manager import BlacklistManager

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

BlacklistManager().initialize_redis(app, redis_instance)
initialize_token_in_blacklist_loader(jwt)
initialize_resources(app)

if __name__ == "__main__":
    app.run()
