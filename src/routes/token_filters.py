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

cluster = MongoClient(os.getenv('MONGO_DB_SRV'), connect=False)
db = cluster["tokens"]
collection = db["token-filters"]

token_filters = Blueprint('token_filters', __name__,
                          template_folder='templates')


@token_filters.route("/token-filters", methods=["GET", "POST"])
def get_token_filters():
    if request.method == 'GET':
        token_filters = list(collection.find({}))
        return json.dumps(token_filters, default=json_util.default)
