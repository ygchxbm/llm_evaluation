import json
import time
import datetime
from app.serializer.common import Success, NotFoundError, ServerError
from app.log import Log
from ..models.exam import Exam
from ..models.exam_detail import ExamDetail
from ..models.question import Question
from ..models.llm_model import LlmModel
from ..util.chatgpt import completions_api


def exam_detail(exam_id):
    Log.info('exam_detail')

    exam = Exam.get(exam_id)
    if exam is None:
        return NotFoundError()
    exam = exam.to_dict()

    llm_model = LlmModel.get(exam['llm_model_id'])
    if exam is None:
        return NotFoundError()
    exam['llm_model_name'] = llm_model.name

    questions = Question.list(exam['question_set_id'])
    questions = [question.to_dict() for question in questions]
    exam['questions'] = questions

    answers = ExamDetail.list(exam['id'])
    answers = [answer.to_dict() for answer in answers]
    exam['my_answers'] = answers

    other_models = LlmModel.list_4_not_ids([exam['llm_model_id']])
    other_model_ids = [model.id for model in other_models]
    other_exams = Exam.list(other_model_ids)
    other_exam_ids = [exam.id for exam in other_exams]
    question_ids = [question['id'] for question in questions]
    other_answers = ExamDetail.list_4_other_answers(other_exam_ids, question_ids)
    for i in range(len(other_answers)):
        other_answers[i]['llm_model_name'] = ''
        for other_model in other_models:
            if other_model.id == other_answers[i]['llm_model_id']:
                other_answers[i]['llm_model_name'] = other_model.name
                break
    other_answers = [other_answer.to_dict() for other_answer in other_answers]

    exam['other_answers'] = other_answers

    return Success(exam)


def generate_answer(exam_id, question_id, current_user):
    Log.info('generate_answer')

    exam = Exam.get(exam_id)
    if exam is None:
        return NotFoundError()

    llm_model = LlmModel.get(exam.llm_model_id)
    if exam is None:
        return NotFoundError()

    answer = ExamDetail.get_answer(exam_id, question_id, current_user['id'])

    if answer is None:
        question = Question.get(question_id)
        if question is None:
            return NotFoundError()
        question_str = question.question
        dimension = question.dimension
        llm_gen_count = 1
        detailId = 0
    else:
        question_str = answer.question
        dimension = answer.dimension
        llm_gen_count = answer.llm_gen_count + 1
        detailId = answer.id

    start_time = time.time()
    status_code, text, answer = completions_api(llm_model.model_name, [{'role': 'user', 'content': question_str}])
    if status_code != 200:
        return ServerError(text)

    llm_answer = answer
    llm_timecost = (time.time() - start_time) * 1000
    exam_detail_id = ExamDetail.save_llm_answer(detailId, exam_id, question_id, question_str, dimension, llm_answer, llm_timecost, llm_gen_count, current_user['id'], current_user['name'])

    exam_detail = ExamDetail.get(exam_detail_id)
    if exam_detail is None:
        return NotFoundError()

    return Success(exam_detail.to_dict())


def submit_score(exam_detail_id, submit_score, submit_remark, submit_timecost, current_user):
    Log.info('submit_score')

    exam_detail = ExamDetail.get(exam_detail_id)
    if exam_detail is None:
        return NotFoundError("没有找到评测详情")

    exam = Exam.get(exam_detail.exam_id)
    if exam is None:
        return NotFoundError("没有找到评测")

    ExamDetail.update_submit(exam_detail.id, submit_score, current_user['id'], current_user['name'], datetime.datetime.now(), submit_remark, submit_timecost)

    # 检查是否是最后一题
    done_count = ExamDetail.get_finished_submit_count(exam_detail.exam_id, current_user['id'])
    if exam.question_count <= done_count:
        _update_model_score(exam.llm_model_id)
        _update_exam_submit_count_and_score(exam.id)

    return Success("success")


def _update_model_score(llm_model_id):
    exams = Exam.list_4_model(llm_model_id)
    exam_ids = [exam.id for exam in exams]

    results = ExamDetail.get_submit_score(exam_ids)

    score_sum = 0
    score_cnt = 0
    score_detail = {}
    score_detail_question_set = {}
    question_set_exam_id = {}

    for i in range(len(results)):
        result = results[i]
        score_sum += result[0]
        score_cnt += result[1]
        dimension = result[2]
        exam_id = result[3]
        question_set_id = 0
        for exam in exams:
            if exam.id == exam_id:
                question_set_id = exam.question_set_id
                break

        if dimension not in score_detail:
            score_detail[dimension] = {'cnt': 0, 'score': 0}
        score_detail[dimension]['score'] += result[0]
        score_detail[dimension]['cnt'] += result[1]

        if question_set_id > 0:
            if question_set_id not in score_detail_question_set:
                score_detail_question_set[question_set_id] = {'cnt': 0, 'score': 0}
            score_detail_question_set[question_set_id]['score'] += result[0]
            score_detail_question_set[question_set_id]['cnt'] += result[1]

            if question_set_id not in question_set_exam_id:
                question_set_exam_id[question_set_id] = []
            question_set_exam_id[question_set_id].append(exam_id)

    for k, v in score_detail.items():
        score_detail[k] = v['score'] / v['cnt']

    for k, v in score_detail_question_set.items():
        score_detail_question_set[k] = v['score'] / v['cnt']

    score_detail_str = json.dumps(score_detail, ensure_ascii=False, default=float)

    score_detail_question_set_str = json.dumps(score_detail_question_set, ensure_ascii=False, default=float)

    question_set_exam_id_str = json.dumps(question_set_exam_id, ensure_ascii=False, default=float)

    LlmModel.update_submit(llm_model_id, len(exam_ids), score_sum/score_cnt, score_detail_str, score_detail_question_set_str, question_set_exam_id_str)


def _update_exam_submit_count_and_score(exam_id):
    exam = Exam.get(exam_id)

    results = ExamDetail.get_submit_score_by_user_id(exam_id)
    submit_score= 0
    submit_count = 0
    for i in range(len(results)):
        result = results[i]
        submit_score += result[0]
        submit_count += result[1]
    submit_score = submit_score/len(results)

    Exam.update_submit_count(exam.id, submit_count, submit_score)
