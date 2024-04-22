import os
from flask import Blueprint
from flask_jwt_extended import jwt_required
from ..functions.handler import handler

import datetime as dt
import pytz
import requests


jupiter_tokens_cron = Blueprint('jupiter_tokens_cron', __name__,
                                  template_folder='templates')

@jupiter_tokens_cron.route("/tasks/v2/jupiter-tokens-cron", methods=["GET"])
@jwt_required()
def get_jupiter_tokens_cron():
    print(f'Jupiter Tokens Cron Started at: {dt.datetime.now(pytz.utc)}')
    handler()
    print(
        f'Jupiter Tokens Cron Finished at: {dt.datetime.now(pytz.utc)}')
    return 'Jupiter Tokens Cron successful'
