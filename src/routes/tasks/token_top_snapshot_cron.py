from flask import Blueprint
from flask_jwt_extended import jwt_required
from ...schedulers.functions.get_token_top_snapshot import get_top_token_snapshot_and_post_concurrently

import datetime as dt
import pytz

token_top_snapshot_cron = Blueprint('token_top_snapshot_cron', __name__,
                                    template_folder='templates')

@token_top_snapshot_cron.route("/tasks/token-top-snapshot-cron", methods=["GET"])
@jwt_required()
def get_token_top_snapshot_cron():
    print('Token Top Snapshot Scheduler Started')
    get_top_token_snapshot_and_post_concurrently()
    print(f'Token Top Snapshot Scheduler Finished at: {dt.datetime.now(pytz.utc)}')
    return 'Token top snapshot cron successful'
