from flask import Blueprint
import time

from flask_jwt_extended import jwt_required


test_route = Blueprint('test_route', __name__,
                       template_folder='templates')


@test_route.route("/tasks/test/<dur>", methods=["GET"])
@jwt_required()
def get_test_route(dur):
    print(f'sleeping for {dur} seconds')
    time.sleep(int(dur))
    print('finished sleeping')
    return 'Test task successful'
