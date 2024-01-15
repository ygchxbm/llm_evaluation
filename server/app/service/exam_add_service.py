from app.serializer.common import Success, NotFoundError, ServerError
from app.log import Log
from ..models.exam import Exam
from ..models.llm_model import LlmModel
from ..models.question_set import QuestionSet
from ..models.question import Question


def exam_add_service(question_set_id, llm_model_id, deadline, current_user):
    Log.info('exam_add_service')

    llm_model = LlmModel.get(llm_model_id)
    if llm_model is None:
        return NotFoundError('LlmModel not found')

    question_set = QuestionSet.get(question_set_id)
    if question_set is None:
        return NotFoundError('QuestionSet not found')

    questions = Question.list(question_set_id)
    if questions is None:
        return NotFoundError('Question not found')

    current_user_name = ''
    if current_user['name'] is not None:
        current_user_name = current_user['name']
    exam = Exam.add(current_user['id'], current_user_name, deadline, llm_model_id, question_set_id, len(questions), 0)
    if not exam:
        return ServerError('exam add error')

    return Success(exam.to_dict())