import os
from flask import Flask
from flask import request
from flask_jwt_extended import JWTManager
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import pandas as pd
import numpy as np
from src.routes.auth import auth
from src.routes.default_route import default_route
from src.routes.token_metadata import token_metadata
from src.routes.token_timeseries import token_timeseries
from src.routes.token_top_snapshot import token_top_snapshot
from src.routes.substr_search import substr_search
from src.routes.token_filters import token_filters
from src.routes.users import users
from src.routes.tasks.test import test_route
from src.routes.tasks.token_timeseries_cron import token_timeseries_cron
from src.routes.tasks.token_top_snapshot_cron import token_top_snapshot_cron
from src.routes.tasks.token_filters_cron import token_filters_cron
from src.routes.tasks.batch_update_user_leaderboards_cron import batch_update_user_leaderboards_cron
from src.routes.tasks.update_token_list_cron import update_token_list_cron
from src.routes.tasks.update_user_snapshot_cron import update_user_snapshot_cron
from src.routes.tasks.update_substr_search_cron import update_substr_search_cron
from src.routes.tasks.jupiter_timeseries_cron.route.jupiter_timeseries_cron import jupiter_timeseries_cron
from src.routes.tasks.v2.jupiter_tokens_cron.route.jupiter_tokens_cron import jupiter_tokens_cron
from src.routes.tasks.v2.delete_old_historical_entries_cron.route.delete_old_historical_entries_cron import delete_old_historical_entries_cron

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 
jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(default_route)
app.register_blueprint(token_metadata)
app.register_blueprint(token_timeseries)
app.register_blueprint(token_top_snapshot)
app.register_blueprint(substr_search)
app.register_blueprint(token_filters)
app.register_blueprint(users)
app.register_blueprint(test_route)
app.register_blueprint(token_timeseries_cron)
app.register_blueprint(token_top_snapshot_cron)
app.register_blueprint(token_filters_cron)
app.register_blueprint(batch_update_user_leaderboards_cron)
app.register_blueprint(update_token_list_cron)
app.register_blueprint(update_user_snapshot_cron)
app.register_blueprint(update_substr_search_cron)
app.register_blueprint(jupiter_timeseries_cron)
app.register_blueprint(jupiter_tokens_cron)
app.register_blueprint(delete_old_historical_entries_cron)


# if os.environ.get('FLASK_ENV') == 'production':
#     if __name__ == '__main__':
#         app.run(debug=False)
# else:
#     if __name__ == "__main__":
#         app.run(debug=True, port=5000, host="0.0.0.0")
if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")