from flask import Blueprint
from flask_jwt_extended import jwt_required
from ...schedulers.functions.get_token_filters import get_token_filters_and_post_concurrently

import datetime as dt
import pytz

token_filters_cron = Blueprint('token_filters_cron', __name__,
                               template_folder='templates')


@token_filters_cron.route("/tasks/token-filters-cron", methods=["GET"])
@jwt_required()
def get_token_filters_cron():
    print('Token Filters Scheduler Started')
    get_token_filters_and_post_concurrently()
    print(
        f'Token Filters Scheduler Finished at: {dt.datetime.now(pytz.utc)}')
    return 'Token timeseries cron successful'
