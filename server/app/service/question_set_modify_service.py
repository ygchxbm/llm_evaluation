from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.question_set import QuestionSet


def question_set_modify(question_set_id, name, current_user):
    Log.info('question_set_modify')

    if question_set_id is None:
        question_set_id = 0

    question_set_id = QuestionSet.save(question_set_id, name, current_user['id'], current_user['name'])
    question_set = QuestionSet.get(question_set_id)
    if not question_set:
        raise NotFoundError('QuestionSet not found')

    return Success(question_set.to_dict())