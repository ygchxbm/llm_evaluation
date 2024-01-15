from app.serializer.common import Success, ServerError
from app.log import Log
from ..models.question_set import QuestionSet


def question_set_delete(question_set_id, current_user):
    Log.info('question_set_delete')

    result = QuestionSet.delete(question_set_id, current_user['id'], current_user['name'])
    if not result:
        return ServerError("删除失败")

    return Success("删除成功")