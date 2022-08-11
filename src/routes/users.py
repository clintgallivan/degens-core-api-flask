from flask import Flask, Blueprint
from flask import request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import pandas as pd
import numpy as np

cluster = MongoClient(
    "mongodb+srv://cgallivan:P%40perless2020@cluster0.r1pdh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["tokens"]
collection = db["users"]

users = Blueprint('users', __name__,
                  template_folder='templates')


@users.route("/users", methods=["GET"])
def get_users():
    all_users = list(collection.find({}))
    return json.dumps(all_users, default=json_util.default)
