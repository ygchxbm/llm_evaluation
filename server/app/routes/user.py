
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from app.log import Log
from app.service import login_service, user_list_service
from app.serializer.common import Success, NotFoundError

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/login', methods=['POST'])
def login():

    Log.info('recv user_bp login request type:{}'.format(request.method))

    code = request.form.get('code')
    if code is None or len(code) == 0:
        raise NotFoundError('code is empty')
    redirect_uri = request.form.get('redirect_uri')
    if redirect_uri is None or len(redirect_uri) == 0:
        raise NotFoundError('redirect_uri is empty')

    return login_service.login(code, redirect_uri)


@user_bp.route('/me', methods=['GET'])
@jwt_required()
def me():

    Log.info('recv user_bp me request type:{}'.format(request.method))

    current_user = get_jwt_identity()
    if current_user is None:
        return NotFoundError("没有找到用户")

    return Success(current_user)

@user_bp.route('/list', methods=['GET'])
@jwt_required()
def user_list():

    Log.info('recv user_bp user_list request type:{}'.format(request.method))

    return user_list_service.user_list()
