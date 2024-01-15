from flask import jsonify
from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.llm_model import LlmModel


def llm_model_list():
    Log.info('llm_model_list')

    llm_model_list = LlmModel.list([])
    llm_model_list = [llm_model.to_dict() for llm_model in llm_model_list]

    return Success(llm_model_list)