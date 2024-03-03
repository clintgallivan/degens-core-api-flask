from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

default_route = Blueprint('default_route', __name__, template_folder='templates')

@default_route.route("/", methods=["GET"])
@jwt_required()
def get_default_route():
    return jsonify({
        'status': 'success',
        'message': 'Degens core api up and running!'
    })