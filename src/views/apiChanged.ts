import request from '@/utils/request';


/**
 * 题目字段
 * 维度 问题 返回答案 参考答案 分数
 */
export interface Question {
    id: number;
    set_id: number;
    question: string;
    dimension: string;
    answer: string;
    // reference_answers:referenceAnswerItem[];

}

export interface referenceAnswerItem {
    model: string;
    answer: string;
    score: number;
}

export interface answerDetailItem {
    dimension: string;
    exam_id: number;
    id: number;
    llm_answer: string;
    llm_gen_count: number;
    llm_timecost: number;
    question: string;
    question_id: number;
    submit_count: number;
    submit_remark: string;
    submit_score: number;
    submit_time: string;
    submit_timecost: number;
    submit_user: string;
}

export interface modelGrade {
    modelName: string;
    averageGrade: number;
    comment: string;
    dimension: string;
}

export interface modelItem {
    id: number;
    name: string;
    score: number;
    score_detail: string;
    conclusion: string;
}

export interface questionSetItem {
    id: number;
    name: string;
    create_user: string;
    create_time: string;
    questions: Question[];
}

export interface examItem {
    create_ime: string;
    create_user: string;
    deadline: string;
    id: number;
    llm_model: number;
    my_answers: answerDetailItem[];
    other_answers: answerDetailItem[];
    question_count: number;
    question_set_id: number;
    questions: Question[];

}

let questionListCache: Question[] | null = null;
let questionListLoading = false;
let questionListTask: Function[][] = []

/**
 * 获取后台数据，展示问题列表
 */
export function questionList(useCache = true): Promise<Question[]> {
    if (useCache && questionListCache) {
        return Promise.resolve(questionListCache);
    }
    if (questionListLoading) {
        return new Promise((resolve, reject) => {
            questionListTask.push([resolve, reject]);
        })
    }
    npcListLoading = true;
    return request('/todoURL').then(res => {
        questionListCache = res as unknown as Question[];
        questionListLoading = false;
        questionListTask.forEach(cb => cb[0](questionListCache));
        return questionListCache;
    }).catch(e => {
        questionListLoading = false;
        questionListTask.forEach(cb => cb[1](e));
        return Promise.reject(e);
    });
}


export interface Npc {
    id: number;
    parent_id: number;
    name: string;
    avatar: string;
    poster: string;
    personality_data: string;
    world_base_knowledge: string;
    location_knowledge: string;
    model_id?: string;
}

export interface Setting {
    personality_data: string;
    world_base_knowledge: string;
    location_knowledge: string;
}


let npcListCache: Npc[] | null = null;
let npcListLoading = false;
const npcListTasks: Function[][] = [];

export function npcList(useCache = true): Promise<Npc[]> {
    if (useCache && npcListCache) {
        return Promise.resolve(npcListCache);
    }
    if (npcListLoading) {
        return new Promise((resolve, reject) => {
            npcListTasks.push([resolve, reject]);
        })
    }
    npcListLoading = true;
    return request('/oasisme_npc.npcList').then(res => {
        npcListCache = res as unknown as Npc[];
        npcListLoading = false;
        npcListTasks.forEach(cb => cb[0](npcListCache));
        return npcListCache;
    }).catch(e => {
        npcListLoading = false;
        npcListTasks.forEach(cb => cb[1](e));
        return Promise.reject(e);
    });
}

/**
 * * 修改模型名字或评价：POST modifyLlmModel，参数id、name、conclusion，name或conclusion不传表示不修改
 * @param {modelName,judge}
 * @returns {isSuccessful}
 */
export function modifyLlmModel(id: number, conclusion: string) {
    return request(`llm_evaluation.modifyLlmModel?site=llm_evaluation`, {method: 'POST', data: {id: id, conclusion: conclusion}});
}

/**
 *
 * @param
 * @returns {modelName,dimensionsGrade,totalgrade,judge}
 */
/**模型列表：GET llmModelList
 *
 * @returns {modellist[],groupList[]}
 */
let modelListCache: modelItem[] | null = null;

export function modelList(): Promise<modelItem[]> {
    // return request('llm_evaluation.llmModelList?site=llm_evaluation').then(res =>{
    return request('llm_model/list?site=llm_evaluation').then(res => {
            modelListCache = res as unknown as modelItem[];
            const {code, data} = res;
            if (code === 0) {
                // console.info("data:", data)
                return data;
            }
            // console.log(modelListCache)
            // return modelListCache;
        }
    )
}

let questionSetListCache: questionSetItem[] | null = null;

export function questionSetList(): Promise<questionSetItem[]> {
    // return request('llm_evaluation.questionSetList?site=llm_evaluation').then(res=>{
    return request('question_set/list?site=llm_evaluation').then(res => {
        questionSetListCache = res as unknown as questionSetItem[];
        const {code, data} = res;
        if (code === 0) {
            // console.info("data:", data)
            return data;
        }
        // console.log(questionSetListCache)
        // return questionSetListCache;
    })
}

/**
 * @param {groupName,modelName}
 * @returns {questionGroup[questionItem]}
 */

/**
 * @param {questionGroup[questionItem]}
 * @returns {isSeccessful}
 */
/**
 * @param {groupName}
 * @returns {isDeleted}
 */
/**
 * @returns {groupName[],groupLists[groupList[questionItem]]}
 */
let questionsListCache: Question[] | null = null

export function questionSetDetail(id: number): Promise<Question[]> {
    // return request(`llm_evaluation.questionSetDetail?site=llm_evaluation&id=${id}`).then(res=>{
    return request(`question_set/detail?site=llm_evaluation&set_id=${id}`).then(res => {
        questionsListCache = res.questions as unknown as Question[];
        // console.info("res:", res);
        const {code, data} = res;
        if (code === 0) {
            // console.info("data:", data);
            return data.questions;
        }
        // console.log(questionsListCache)
        // return questionsListCache;
    })
}

/**
 * @param {groupList}
 * @returns {isUpload}
 */
/**
 * 发起评测
 * @param {question_set_id,model_id,deadline}
 * @return {id}
 */
export function createExam(questionSetId: number, modelId: number, deadline?: string): Promise<number> {
    // return request(`llm_evaluation.createExam?site=llm_evaluation`, { method: 'POST', data: { question_set_id:questionSetId,llm_model:modelId } }).then(res => res as unknown as number);
    const formData = new URLSearchParams()
    formData.append('set_id', String(questionSetId));
    formData.append('llm_model_id', String(modelId));
    return request(`exam/add?site=llm_evaluation`, {method: 'POST', headers: {'Content-type': 'application/x-www-form-urlencoded; charset=;UTF-8'}, data: formData})
        .then(res => {
                const {data} = res;
                return res.data.id as unknown as number;
            }
        );
}

/**
 * 评测详情
 * @param{id}
 * @return {questions,my_answers}
 */
let examItemCache: examItem | null = null

//todo:在返回id正常后把id=1改成形参
export function examDetail(id: number): Promise<examItem> {
    // return request(`llm_evaluation.examDetail?site=llm_evaluation&id=${id}`).then(res=>{
    return request(`exam/detail?site=llm_evaluation&exam_id=${id}`).then(res => {
        examItemCache = res.data as unknown as examItem;
        return examItemCache;
    })
}

/**
 * * 导入题库：POST importQuestions?id=xxx，同时通过附件形式上传题库，导入模板可通过导出题库获得
 */
export function importQuestions(id: number, file: File) {
    const formData = new FormData();
    // formData.append('file', file);
    // return request(`llm_evaluation.importQuestions?id=${id}&site=llm_evaluation`, {method: 'POST', data: formData});
    formData.append('set_id', id.toString());
    formData.append('file_data', file)
    return request(`question/import_question?site=llm_evaluation`, {method: 'POST', headers: {'Content-type': 'application/x-www-form-urlencoded; charset=;UTF-8'}, data: formData});
}

/**
 * 生成答案
 * @param exam_id
 * @param question_id
 */
export function generateAnswer(exam_id: number, question_id: number) {
    // return request(`llm_evaluation.generateAnswer?site=llm_evaluation`, {method: 'POST', data: {exam_id: exam_id, question_id: question_id}})
    return request(`exam_detail/generate_answer?site=llm_evaluation&exam_id=${exam_id}&question_id=${question_id}`)
}

/**
 *    * 提交某道题的评分：POST submitScore，
 * 参数exam_detail_id=评测详情id, submit_score=分数0~10, submit_remark=备注, submit_timecost=评测花费时间（前端自动计算，即这道题他打分花了多少时间，单位毫秒）
 * @param exam_detail_id
 * @param submit_score
 * @param submit_timecost
 * @param submit_remark
 * @returns
 */
export function submitScore(exam_detail_id: number, submit_score: number, submit_timecost: number, submit_remark?: string) {
    // return request(`llm_evaluation.submitScore?site=llm_evaluation`, {
    //     method: 'POST',
    //     data: {exam_detail_id: exam_detail_id, submit_score: submit_score, submit_timecost: submit_timecost, submit_remark: submit_remark}
    // })
    const formData=new FormData();
    formData.append('exam_detail_id',exam_detail_id.toString());
    formData.append('submit_score',submit_score.toString());
    formData.append('submit_remark',submit_remark);
    formData.append('submit_timecost',submit_timecost.toString());
    return request(`exam_detail/submit_score?site=llm_evaluation`, {
        method: 'POST',
        headers: {'Content-type': 'application/x-www-form-urlencoded; charset=;UTF-8'},
        data: formData
    })
}

/**
 *导出题库：GET exportQuestions?id=xxx&_optype=export 加上_optype就是导出excel了
 * @returns
 */
export function exportQuestions(id: number) {
    // return `/api/llm_evaluation.exportQuestions?id=${id}&site=llm_evaluation&_optype=export`;
    // return request(`question/export_question?set_id=${id}&site=llm_evaluation&_optype=export`);
    return `http://192.168.110.3:5000/api/question/export_question?set_id=${id}&site=llm_evaluation&_optype=export`;
}

/**
 *  修改/新增题库：POST modifyQuestionSet，参数id、name。有id为修改题库名称，无id参数为新增题库
 * @param [id]
 * @param name
 */
export function modifyQuestionSet(id: string | undefined, name: string) {
    // return request(`llm_evaluation.modifyQuestionSet?site=llm_evaluation`, {method: 'POST', data: {name: name}})
    const formData = new FormData();
    if (typeof id === "string") {
        formData.append('set_id', id);
    }
    formData.append('name', name);
    return request(`/question_set/modify?site=llm_evaluation`, {method: 'POST', headers: {'Content-type': 'application/x-www-form-urlencoded; charset=;UTF-8'}, data: formData})
}

export function npcDetail(id: number): Promise<Npc> {
    return request('/oasisme_npc.npcDetail?id=' + id).then(res => res as unknown as Npc);
}

export function saveNpc(npc: Npc): Promise<number> {
    return request('/oasisme_npc.saveNpc', {method: 'POST', data: {data: npc}}).then(res => res as unknown as number);
}

export function getSetting(): Promise<Setting> {
    return request('/llm_evaluation.getSetting?site=llm_evaluation').then(res => res as unknown as Setting);
}

export function saveSetting(setting: Setting) {
    return request('/oasisme_npc.saveSetting', {method: 'POST', data: {setting}});
}

export interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export interface MessageReply {
    text: { sourceType: string; text: string };
}

export function chat(npcId: number | string, msg: string, sessionId: string, signal?: AbortController) {
    return request('/oasisme_npc.chat', {method: 'POST', data: {npcId, msg, sessionId}, signal: signal?.signal}).then(res => res as unknown as MessageReply);
}

export type FileTuneDataType = 'multiple' | 'single';

export function exportFineTune(id: number, dataType: FileTuneDataType) {
    return `/api/oasisme_npc.exportFineTune?id=${id}&data_type=${dataType}&site=oasisme_npc&_optype=export`;
}

export function importFineTune(id: number, dataType: FileTuneDataType, mode: 'replace' | 'insert', file: File) {
    const formData = new FormData();
    formData.append('id', `${id}`);
    formData.append('data_type', dataType);
    formData.append('mode', mode);
    formData.append('file', file);
    return request('/oasisme_npc.importFineTune', {method: 'POST', data: formData});
}

export function uploadFile(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return request('/common.uploadFile', {method: 'POST', data: formData});
}

export function deleteNpc(id: number): Promise<boolean> {
    return request('/oasisme_npc.deleteNpc', {method: 'POST', data: {id}}).then(res => res as unknown as boolean);
}
