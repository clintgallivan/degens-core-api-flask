import os
from flask import Flask, Blueprint
from flask import request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import pandas as pd
import numpy as np
import datetime as dt
import pytz

cluster = MongoClient(host=os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster["tokens"]
collection = db["token-top-snapshot"]

token_top_snapshot = Blueprint('token_top_snapshot', __name__,
                               template_folder='templates')


@token_top_snapshot.route("/token-top-snapshot", methods=["GET", "POST"])
def get_token_snapshot():
    if request.method == 'GET':
        all_top_tokens = list(collection.find({}))
        return json.dumps(all_top_tokens, default=json_util.default)
