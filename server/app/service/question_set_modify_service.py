from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.question_set import QuestionSet


def question_set_modify(question_set_id, name, current_user):
    Log.info('question_set_modify')

    result = QuestionSet.modify(question_set_id, name, current_user.id, current_user.name)
    if not result:
        raise NotFoundError('QuestionSet not found')

    return Success()