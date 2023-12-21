from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.llm_model import LlmModel


def llm_model_list():
    Log.info('llm_model_list')

    llm_model_list = LlmModel.list()

    return Success(llm_model_list)