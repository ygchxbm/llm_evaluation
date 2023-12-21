
from flask import Blueprint, request, jsonify
from app.log import Log
from app.service import login_service

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/login', methods=['POST'])
def login():

    Log.info('recv llm_model_bp list request type:{}'.format(request.method))

    user_id = request.json.get('user_id', None)
    if user_id is None or user_id <= 0:
        return jsonify(msg='user_id error')

    return login_service.login(user_id)
