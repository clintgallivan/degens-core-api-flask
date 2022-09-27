
# # import apscheduler
# # from apscheduler.schedulers.blocking import BlockingScheduler
# from functions.get_token_timestamp import get_token_list, get_token_timestamp_and_post_concurrently
# import time
# # token_id_list = ['rocket-pool']
# token_id_list = get_token_list()
# # time.sleep(5)


# # sched = BlockingScheduler()


# # @sched.scheduled_job('interval', days=1)
# def function():
#     get_token_timestamp_and_post_concurrently(token_id_list[0:])
#     print('script finished')
#     # get_token_metadata_and_post_concurrently(['astrals-glxy'])


# function()


import apscheduler
import time
import caffeine
from apscheduler.schedulers.blocking import BlockingScheduler
from functions.get_token_timestamp import get_token_list, get_token_timestamp_and_post_concurrently
import datetime as dt
import pytz

caffeine.on(display=False)
token_id_list = get_token_list()


sched = BlockingScheduler()


@sched.scheduled_job('interval', start_date='2022-09-25 03:00:00', days=1, misfire_grace_time=10000)
def function():
    print('Token Timestamp Scheduler Started')
    get_token_timestamp_and_post_concurrently(token_id_list)
    print(
        f'Token Timestamp Scheduler Finished at: {dt.datetime.now(pytz.utc)}')


sched.start()
