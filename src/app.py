"""
  Flask App
"""
import os

import redis
from flask_jwt_extended import JWTManager
from src import create_app
from src import db
from src.resources import initialize_expired_token_callback
from src.resources import initialize_invalid_token
from src.resources import initialize_resources
from src.resources import initialize_revoke_token_callback
from src.resources import initialize_token_in_blacklist_loader
from src.utils.blacklist import BlacklistManager

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


redis_instance = redis.Redis(
    host=os.environ["REDIS_HOST"], port=os.environ["REDIS_PORT"]
)
BlacklistManager().initialize_redis(app, redis_instance)
initialize_token_in_blacklist_loader(jwt)
initialize_invalid_token(jwt)
initialize_expired_token_callback(jwt)
initialize_revoke_token_callback(jwt)
initialize_resources(app)

if __name__ == "__main__":
    app.run()
