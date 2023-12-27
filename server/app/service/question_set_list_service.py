from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.question_set import QuestionSet


def question_set_list():
    Log.info('question_set_list')

    question_set_list = QuestionSet.list([])

    return Success(question_set_list)