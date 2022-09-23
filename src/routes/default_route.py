from flask import Blueprint

default_route = Blueprint('default_route', __name__,
                          template_folder='templates')


@default_route.route("/", methods=["GET"])
def get_default_route():
    return 'Degens core api up and running!'
