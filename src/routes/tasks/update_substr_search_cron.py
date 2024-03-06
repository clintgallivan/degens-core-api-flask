from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from ...schedulers.functions.update_substr_search_data import get_token_substr_data_and_post_concurrently

import datetime as dt
import pytz

update_substr_search_cron = Blueprint('update_substr_search_cron', __name__,
                                  template_folder='templates')


@update_substr_search_cron.route("/tasks/update-substr-search-cron", methods=["GET"])
@jwt_required()
def get_token_timeseries_cron():
    print('Update Substr Search Scheduler Started')
    get_token_substr_data_and_post_concurrently()
    print(
        f'Update Substr Search Scheduler Finished at: {dt.datetime.now(pytz.utc)}')
    return jsonify({
        'status': 'success',
        'message': 'Finished updating substr-search collection in db'
    })
