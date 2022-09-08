from flask import Flask
from flask import request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import pandas as pd
import numpy as np
from src.routes.token_metadata import token_metadata
from src.routes.token_timeseries import token_timeseries
from src.routes.token_top_snapshot import token_top_snapshot
from src.routes.substr_search import substr_search
from src.routes.token_filters import token_filters
from src.routes.users import users

app = Flask(__name__)

app.register_blueprint(token_metadata)
app.register_blueprint(token_timeseries)
app.register_blueprint(token_top_snapshot)
app.register_blueprint(substr_search)
app.register_blueprint(token_filters)
app.register_blueprint(users)


if __name__ == "__main__":
    app.run(debug=True, port=6000, host="0.0.0.0")
