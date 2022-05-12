
import apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler
# import functions

# declare any pre-function calls

sched = BlockingScheduler()


@sched.scheduled_job('interval', days=1)
def function():
    # call functions here


sched.start()
