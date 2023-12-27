from app.serializer.common import Success, NotFoundError
from app.log import Log
from ..models.exam import Exam
from ..models.exam_detail import ExamDetail
from ..models.question import Question
from ..models.llm_model import LlmModel
from ..models.user import User


def exam_detail(id):
    Log.info('exam_detail')

    exam = Exam.get(id)
    if exam is None:
        return NotFoundError()

    llm_model = LlmModel.get(exam.llm_model_id)
    exam.llm_model_name = llm_model.name

    questions = Question.list(exam.question_set_id)
    exam.questions = questions

    answers = ExamDetail.list(exam.id)
    exam.answers = answers

    other_models = LlmModel.list_4_not_ids([exam.llm_model_id])
    other_model_ids = [model.id for model in other_models]
    other_exams = Exam.list(other_model_ids)
    other_exam_ids = [exam.id for exam in other_exams]
    question_ids = [question.id for question in questions]
    other_answers = ExamDetail.list_4_other_answers(other_exam_ids, question_ids)
    exam.other_answers = other_answers

    for i in range(exam.other_answers):
        exam.other_answers[i]['llm_model_name'] = ''
        for other_model in other_models:
            if other_model.id == exam.other_answers[i]['llm_model_id']:
                exam.other_answers[i]['llm_model_name'] = other_model.name
                break

    return Success(exam)
