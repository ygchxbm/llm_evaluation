
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.log import Log
from app.service import exam_list_service, exam_detail_service, exam_add_service

exam_bp = Blueprint('exam_bp', __name__)


@exam_bp.route('/list', methods=['GET'])
@jwt_required()
def exam_list():

    Log.info('recv exam_bp exam_list request type:{}'.format(request.method))

    page_num = request.args.get('page_num', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    llm_model_id = request.args.get('llm_model_id', 0, type=int)
    create_user_id = request.args.get('create_user_id', 0, type=int)
    created_time_min = request.args.get('created_time_min', 0, type=int)
    created_time_max = request.args.get('created_time_max', 0, type=int)

    return exam_list_service.exam_list(page_num, page_size, llm_model_id, create_user_id, created_time_min, created_time_max)


@exam_bp.route('/detail', methods=['GET'])
@jwt_required()
def exam_detail():

    Log.info('recv exam_bp exam_detail request type:{}'.format(request.method))

    exam_id = request.args.get('exam_id', None)
    if exam_id is None:
        return jsonify(msg='exam_id error')
    else:
        exam_id = int(exam_id)

    return exam_detail_service.exam_detail(exam_id)


@exam_bp.route('/add', methods=['POST'])
@jwt_required()
def add():

    Log.info('recv exam_bp add request type:{}'.format(request.method))

    set_id = request.form.get('set_id')
    if set_id is None:
        return jsonify(msg='set_id error')
    else:
        set_id = int(set_id)

    llm_model_id = request.form.get('llm_model_id')
    if llm_model_id is None:
        return jsonify(msg='llm_model_id error')
    else:
        llm_model_id = int(llm_model_id)

    deadline = request.form.get('deadline')

    current_user = get_jwt_identity()

    return exam_add_service.exam_add_service(set_id, llm_model_id, deadline, current_user)
