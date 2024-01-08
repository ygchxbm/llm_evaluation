
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.log import Log
from app.service import question_set_list_service, question_set_detail_service, question_set_modify_service

question_set_bp = Blueprint('question_set_bp', __name__)


@question_set_bp.route('/list', methods=['GET'])
@jwt_required()
def set_list():

    Log.info('recv question_set_bp set_list request type:{}'.format(request.method))

    return question_set_list_service.question_set_list()


@question_set_bp.route('/detail', methods=['GET'])
@jwt_required()
def set_detail():

    Log.info('recv question_set_bp set_detail request type:{}'.format(request.method))

    set_id = request.args.get('set_id', None)
    if set_id is None:
        return jsonify(msg='set_id error')
    else:
        set_id = int(set_id)

    return question_set_detail_service.question_set_detail(set_id)


@question_set_bp.route('/modify', methods=['POST'])
@jwt_required()
def modify():

    Log.info('recv question_set_bp modify request type:{}'.format(request.method))

    set_id = request.form.get('set_id')
    name = request.form.get('name')

    current_user = get_jwt_identity()

    return question_set_modify_service.question_set_modify(set_id, name, current_user)
