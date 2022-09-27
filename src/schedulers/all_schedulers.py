import apscheduler
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from functions.get_token_timestamp import get_token_list, get_token_timestamp_and_post_concurrently
from functions.get_token_top_snapshot import get_top_token_snapshot_and_post_concurrently
from functions.get_token_filters import get_token_filters_and_post_concurrently
import datetime as dt
import pytz

token_id_list = get_token_list()


sched = BlockingScheduler()


# * timeseries scheduler
@sched.scheduled_job('interval', start_date='2022-09-27 09:00:00', days=1, misfire_grace_time=10000)
def function():
    print('Token Timestamp Scheduler Started')
    get_token_timestamp_and_post_concurrently(token_id_list)
    print(
        f'Token Timestamp Scheduler Finished at: {dt.datetime.now(pytz.utc)}')

# * top snapshot scheduler


@sched.scheduled_job('interval', start_date='2022-09-27 21:00:00', days=1, misfire_grace_time=10000)
def function():
    print('Token Snapshot Scheduler Started')
    get_top_token_snapshot_and_post_concurrently()
    print(
        f'Token Snapshot Scheduler Finished at: {dt.datetime.now(pytz.utc)}')

# * token filters scheduler


@sched.scheduled_job('interval', start_date='2022-09-27 08:55:00', days=1, misfire_grace_time=10000)
def function():
    print('Token Filters Scheduler Started')
    get_token_filters_and_post_concurrently()
    print(
        f'Token Filters Scheduler Finished at: {dt.datetime.now(pytz.utc)}')


sched.start()