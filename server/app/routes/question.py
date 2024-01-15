
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.log import Log
from app.service import question_xls_service

question_bp = Blueprint('question_bp', __name__)


@question_bp.route('/import_question', methods=['POST'])
@jwt_required()
def import_xls():
    set_id = request.form.get('set_id')
    if set_id is None:
        return jsonify(msg='set_id error')
    else:
        set_id = int(set_id)

    file_data = request.files.get('file_data')
    if not file_data:
        return jsonify(msg='请上传文件')

    return question_xls_service.import_question(set_id, file_data)


@question_bp.route('/export_question', methods=['GET'])
# @jwt_required()
def export_xls():
    set_id = request.args.get('set_id', None)
    if set_id is None:
        return jsonify(msg='set_id error')
    else:
        set_id = int(set_id)

    return question_xls_service.export_question(set_id)
