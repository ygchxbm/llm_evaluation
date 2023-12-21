
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.log import Log
from app.service import question_set_list_service, question_set_detail_service, question_set_modify_service
import xlrd

question_bp = Blueprint('question_bp', __name__)


@question_bp.route('/import_xls', methods=['POST'])
@jwt_required()
def import_xls():

    Log.info('recv question_bp import_xls request type:{}'.format(request.method))

    set_id = request.args.get('set_id', None)
    if set_id is None:
        return jsonify(msg='set_id error')
    else:
        set_id = int(set_id)

    file = request.files.get('file')
    if file:
        file.save(file.filename)
        workbook = xlrd.open_workbook(file.filename)
        sheet = workbook.sheet_by_index(0)
        for row in range(sheet.nrows):
            print(sheet.row_values(row))
    return '文件上传并解析成功'

    return question_set_list_service.question_set_list()
