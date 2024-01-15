
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.log import Log
from app.service import llm_model_list_service, llm_model_modify_service

llm_model_bp = Blueprint('llm_model_bp', __name__)


@llm_model_bp.route('/list', methods=['GET'])
@jwt_required()
def list():

    Log.info('recv llm_model_bp list request type:{}'.format(request.method))

    return llm_model_list_service.llm_model_list()


@llm_model_bp.route('/modify', methods=['POST'])
@jwt_required()
def modify():

    Log.info('recv llm_model_bp modify request type:{}'.format(request.method))

    llm_model_id = request.json.get('id', None)
    if llm_model_id is None or llm_model_id <= 0:
        return jsonify(msg='llm_model_id error')

    name = request.json.get('name', None)
    conclusion = request.json.get('conclusion', None)

    current_user = get_jwt_identity()

    return llm_model_modify_service.llm_model_modify(llm_model_id, name, conclusion, current_user)