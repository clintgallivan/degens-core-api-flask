from flask import Flask, Blueprint
from flask import request
import pymongo
from pymongo import MongoClient
import json
from bson import json_util
import pandas as pd
import numpy as np

cluster = MongoClient(
    "mongodb+srv://cgallivan:newui123@cluster0.r1pdh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["tokens"]
collection = db["token-metadata"]

token_metadata = Blueprint('token_metadata', __name__,
                           template_folder='templates')


@token_metadata.route("/tokens", methods=["GET"])
def get_token_metadata():
    all_tokens = list(collection.find({}))
    return json.dumps(all_tokens, default=json_util.default)
