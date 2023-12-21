from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.question_set import QuestionSet
from ..models.question import Question


def question_set_detail(id):
    Log.info('question_set_detail')

    question_set = QuestionSet.get(id)
    if question_set is None:
        raise NotFoundError()

    question_list = Question.list(id)

    return Success({
        'question_set': question_set,
        'question_list': question_list,
    })
