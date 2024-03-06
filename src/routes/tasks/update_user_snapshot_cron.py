from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from ...schedulers.functions.update_user_snapshot import update_user_snapshot

import datetime as dt
import pytz

update_user_snapshot_cron = Blueprint('update_user_snapshot_cron', __name__,
                                                template_folder='templates')


@update_user_snapshot_cron.route("/tasks/update-user-snapshot-cron", methods=["GET"])
@jwt_required()
def get_update_user_snapshot_cron():
    print('Update User Snapshot Scheduler Started')
    update_user_snapshot()
    print(
        f'Update User Snapshot Scheduler Finished at: {dt.datetime.now(pytz.utc)}')
    return jsonify({
        'status': 'success',
        'message': 'Finished updating user collection in db'
    })
