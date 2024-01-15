from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.llm_model import LlmModel


def llm_model_modify(llm_model_id, name, conclusion, current_user):
    Log.info('llm_model_modify')

    result = LlmModel.modify(llm_model_id, name, conclusion, current_user.id, current_user.name)
    if not result:
        return NotFoundError()

    return Success()