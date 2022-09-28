import apscheduler
# import caffeine
from apscheduler.schedulers.blocking import BlockingScheduler
from functions.batch_update_user_leaderboards import batch_update_user_leaderboards
import datetime as dt
import pytz

# caffeine.on(display=False)

sched = BlockingScheduler()


@sched.scheduled_job('interval', start_date='2022-09-08 12:35:00', hours=1, misfire_grace_time=10000)
def function():
    print('User Leaderboard Scheduler Started')
    batch_update_user_leaderboards()
    print(
        f'User Leaderbaord Scheduler Finished at: {dt.datetime.now(pytz.utc)}')


sched.start()
