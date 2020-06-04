"""
  Flask App
"""
import datetime
import os

from flask_jwt_extended import JWTManager
from src import create_app
from src import db
from src import redis_instance
from src.resources import initialize_resources
from src.resources import initialize_token_in_blacklist_loader
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


app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
    minutes=int(os.environ["JWT_ACCESS_TOKEN_EXPIRES_MINUTES"])
)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(
    days=int(os.environ["JWT_REFRESH_TOKEN_EXPIRES_DAYS"])
)

BlacklistManager().initialize_redis(app, redis_instance)
initialize_token_in_blacklist_loader(jwt)
initialize_resources(app)

if __name__ == "__main__":
    app.run()
