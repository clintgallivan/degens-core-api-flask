from flask import Blueprint
from ...schedulers.functions.batch_update_user_leaderboards import batch_update_user_leaderboards

import datetime as dt
import pytz

batch_update_user_leaderboards_cron = Blueprint('batch_update_user_leaderboards_cron', __name__,
                                                template_folder='templates')


@batch_update_user_leaderboards_cron.route("/tasks/batch-update-user-leaderboards-cron", methods=["GET"])
def get_batch_update_user_leaderboards_cron():
    print('Batch Update User Leaderboards Scheduler Started')
    batch_update_user_leaderboards()
    print(
        f'Batch Update User Leaderboards Scheduler Finished at: {dt.datetime.now(pytz.utc)}')
    return 'Batch Update User Leaderboards cron successful'
