from flask import Flask, Blueprint
from flask import request
import pymongo
from pymongo import MongoClient, UpdateOne
import json
from bson import json_util
import pandas as pd
import numpy as np
from datetime import datetime
import pytz

cluster = MongoClient(
    "mongodb+srv://cgallivan:P%40perless2020@cluster0.r1pdh.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["tokens"]
collection = db["users"]

users = Blueprint('users', __name__,
                  template_folder='templates')


@users.route("/users/", methods=["GET", "POST"])
def get_users():
    if request.method == 'GET':
        params = request.args.to_dict()
        keys_to_include = {}
        if params.get('cron'):
            keys_to_include = {
                "uid": 1, "portfolio_metadata": 1, "historical.portfolios.season_1": {'$slice': 1}, "historical.portfolios.all_time": {'$slice': 1}}
        all_users = list(collection.find(
            {}, keys_to_include))
        return json.dumps(all_users, default=json_util.default)
    else:
        html_output = ''
        count = 0
        request_payload = request.json
        bulk_requests = []
        for user in request_payload:
            count = count + 1
            portfolio_to_push = {
            }
            for key in user['historical']['portfolios']:
                def str_to_datetime(timestamp_as_str):
                    return datetime.strptime(timestamp_as_str, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=pytz.UTC)
                user['historical']['portfolios'][f'{key}'][0]['timestamp'] = str_to_datetime(
                    user['historical']['portfolios'][f'{key}'][0]['timestamp'])
                portfolio_to_push[f'historical.portfolios.{key}'] = {
                    '$each': [
                        user['historical']['portfolios'][f'{key}'][0],
                    ],
                    '$position': 0
                }
            bulk_requests.append(UpdateOne({'uid': user['uid']}, {
                '$push': portfolio_to_push
            }))
        collection.bulk_write(bulk_requests)
        html_output = f'{count} users were updated!'
        return html_output


@users.route("/users/<uid>", methods=["GET"])
def get_user(uid):
    if not uid:
        all_users = list(collection.find({}))
    else:
        all_users = list(collection.find({'uid': uid}))
    return json.dumps(all_users, default=json_util.default)
