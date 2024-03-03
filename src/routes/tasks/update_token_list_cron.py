from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from ...schedulers.functions.update_token_list import get_token_list_and_update_db_concurrently

import datetime as dt
import pytz

update_token_list_cron = Blueprint('update_token_list_cron', __name__,
                                  template_folder='templates')


@update_token_list_cron.route("/tasks/update-token-list-cron", methods=["GET"])
@jwt_required()
def get_token_timeseries_cron():
    print('Update Token List Scheduler Started')
    get_token_list_and_update_db_concurrently()
    print(
        f'Update Token List Scheduler Finished at: {dt.datetime.now(pytz.utc)}')
    return jsonify({
        'status': 'success',
        'message': 'Finished updating token-list collection in db'
    })
