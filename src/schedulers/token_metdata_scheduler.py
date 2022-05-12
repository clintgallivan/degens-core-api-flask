
# import apscheduler
# from apscheduler.schedulers.blocking import BlockingScheduler
from functions.get_full_metdata import get_token_list, get_token_metadata_and_post_concurrently

token_id_list = []
token_id_list = get_token_list()


# sched = BlockingScheduler()


# @sched.scheduled_job('interval', days=1)
def function():
    get_token_metadata_and_post_concurrently(token_id_list)
    # get_token_metadata_and_post_concurrently(['astrals-glxy'])


function()

# sched.start()
