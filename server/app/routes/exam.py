
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.log import Log
from app.service import exam_list_service, exam_detail_service

exam_bp = Blueprint('exam_bp', __name__)


@exam_bp.route('/list', methods=['GET'])
@jwt_required()
def exam_list():

    Log.info('recv exam_bp exam_list request type:{}'.format(request.method))

    page = request.args.get('page', 1, type=int)

    return exam_list_service.exam_list(page)


@exam_bp.route('/detail', methods=['GET'])
@jwt_required()
def exam_detail():

    Log.info('recv exam_bp exam_detail request type:{}'.format(request.method))

    id = request.args.get('id', None)
    if id is None:
        return jsonify(msg='id error')
    else:
        id = int(id)

    return exam_detail_service.exam_detail(id)


@exam_bp.route('/add', methods=['POST'])
@jwt_required()
def add():

    Log.info('recv exam_bp modify request type:{}'.format(request.method))

    set_id = request.args.get('set_id', None)
    if set_id is None:
        return jsonify(msg='set_id error')
    else:
        set_id = int(set_id)

    name = request.json.get('name', None)

    current_user = get_jwt_identity()

    return question_set_modify_service.question_set_modify(set_id, name, current_user)
