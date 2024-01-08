
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.log import Log
from app.service import exam_detail_service
from app.serializer.common import Success, ParamError

exam_detail_bp = Blueprint('exam_detail_bp', __name__)


@exam_detail_bp.route('/generate_answer', methods=['GET'])
@jwt_required()
def generate_answer():

    Log.info('recv exam_detail_bp generate_answer request type:{}'.format(request.method))

    exam_id = request.args.get('exam_id', None)
    if exam_id is None:
        return jsonify(msg='exam_id error')
    else:
        exam_id = int(exam_id)

    question_id = request.args.get('question_id', None)
    if question_id is None:
        return jsonify(msg='question_id error')
    else:
        question_id = int(question_id)

    current_user = get_jwt_identity()

    return exam_detail_service.generate_answer(exam_id, question_id, current_user)


@exam_detail_bp.route('/submit_score', methods=['POST'])
@jwt_required()
def submit_score():

    Log.info('recv exam_detail_bp submit_score request type:{}'.format(request.method))

    exam_detail_id = request.form.get('exam_detail_id')
    if exam_detail_id is None:
        return jsonify(msg='exam_detail_id error')
    else:
        exam_detail_id = int(exam_detail_id)

    submit_score = request.form.get('submit_score')
    if submit_score is None:
        return jsonify(msg='submit_score error')
    else:
        submit_score = int(submit_score)
    if submit_score < 0 or submit_score > 10:
        return ParamError('Bad Score')

    submit_remark = request.form.get('submit_remark')
    submit_timecost = request.form.get('submit_timecost')

    current_user = get_jwt_identity()

    return exam_detail_service.submit_score(exam_detail_id, submit_score, submit_remark, submit_timecost, current_user)
