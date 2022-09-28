from flask import Blueprint
import time


test_route = Blueprint('test_route', __name__,
                       template_folder='templates')


@test_route.route("/tasks/test/<dur>", methods=["GET"])
def get_test_route(dur):
    print(f'sleeping for {dur} seconds')
    time.sleep(dur)
    print('finished sleeping')
    return 'Test task successful'
