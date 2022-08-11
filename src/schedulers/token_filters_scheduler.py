
# * run this every day

import apscheduler
import time
import caffeine
from apscheduler.schedulers.blocking import BlockingScheduler

from functions.get_token_filters import get_token_filters_and_post_concurrently
import datetime as dt
import pytz

caffeine.on(display=False)


sched = BlockingScheduler()


@sched.scheduled_job('interval', start_date='2022-08-03 02:58:00', days=1, misfire_grace_time=10000)
def function():
    print('Token Filters Scheduler Started')
    get_token_filters_and_post_concurrently()
    print(
        f'Token Filters Scheduler Finished at: {dt.datetime.now(pytz.utc)}')


sched.start()

# yaki-gold yag
