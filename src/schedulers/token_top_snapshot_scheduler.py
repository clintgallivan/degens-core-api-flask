
# # import apscheduler
# # from apscheduler.schedulers.blocking import BlockingScheduler
# from functions.get_token_top_snapshot import get_top_token_snapshot_and_post_concurrently


# # sched = BlockingScheduler()


# # @sched.scheduled_job('interval', days=1)
# def function():
#     get_top_token_snapshot_and_post_concurrently()
#     print('script finished')


# function()


import apscheduler
import caffeine
from apscheduler.schedulers.blocking import BlockingScheduler
from functions.get_token_top_snapshot import get_top_token_snapshot_and_post_concurrently
import datetime as dt
import pytz

caffeine.on(display=False)

sched = BlockingScheduler()


@sched.scheduled_job('interval', start_date='2022-08-04 14:00:00', days=1, misfire_grace_time=10000)
def function():
    print('Token Snapshot Scheduler Started')
    get_top_token_snapshot_and_post_concurrently()
    print(
        f'Token Snapshot Scheduler Finished at: {dt.datetime.now(pytz.utc)}')


sched.start()
