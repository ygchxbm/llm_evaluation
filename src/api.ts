import request from "@/utils/request";

export async function login(code:string){
    const formData = new FormData();
    formData.append('code', code);
    formData.append('redirect_uri', 'https://lightpaw.com/Login');
    return request(`user/login`, {method: 'POST', headers: {'Content-type': 'application/x-www-form-urlencoded; charset=;UTF-8'}, data: formData})
}

//////首页
/**
 * 题库列表的字段
 */
export interface questionSetItem {
    id: number;
    name: string;
    create_user: string;
    create_time: string;
    questions: Question[];
}

let questionSetListCache: questionSetItem[] | null = null;

/**
 * 获取题库list
 */
export async function questionSetList(): Promise<questionSetItem[]> {
    const res = await request('question_set/list?site=llm_evaluation');
    const {data} = res;
    questionSetListCache = data as unknown as questionSetItem[];
    return questionSetListCache
}

/**
 * 一个模型的字段
 */
export interface modelItem {
    id: number;
    name: string;
    score: number;
    score_detail: string;
    conclusion: string;
    //add by hugh
    model_name: string;
    score_detail_question_set: string;
    scale:number;
}


let modelListCache: modelItem[] | null = null;

/**
 * 获取模型列表
 */
export async function modelList(): Promise<modelItem[]> {
    const res = await request('llm_model/list?site=llm_evaluation');
    const {data} = res;
    modelListCache = data as unknown as modelItem[];
    return modelListCache;
}


//////题库管理

/**
 * 一个题库的字段
 * 维度 问题 返回答案 参考答案 分数
 */
export interface Question {
    id: number;
    set_id: number;
    question: string;
    dimension: string;
    answer: string;
    //add by hugh
    questions: questions[];
    name: string;
    // reference_answers:referenceAnswerItem[];
}

export interface questions {
    answer: string;
    created_at: string;
    deleted_at: object;
    dimension: string;
    id: number;
    question: string;
    question_set_id: number;
    updated_at: string;
}

let questionsListCache: Question | null = null

/**
 * 获取一个题库的详情
 */
export async function questionSetDetail(id: number): Promise<Question | null> {
    const res = await request(`question_set/detail?site=llm_evaluation&set_id=${id}`);
    const {data} = res;
    questionsListCache = data as unknown as Question;
    return questionsListCache;
}

export function modifyQuestionSet(id: number | undefined, name: string) {
    const formData = new FormData();
    if (typeof id === "number") {
        formData.append('set_id', id.toString());
    }
    formData.append('name', name);
    return request(`/question_set/modify?site=llm_evaluation`, {method: 'POST', headers: {'Content-type': 'application/x-www-form-urlencoded; charset=;UTF-8'}, data: formData})
}

/**
 * * 导入题库：POST importQuestions?id=xxx，同时通过附件形式上传题库，导入模板可通过导出题库获得
 */
export function importQuestions(id: number, file: File) {
    const formData = new FormData();
    formData.append('set_id', id.toString());
    formData.append('file_data', file)
    return request(`question/import_question?site=llm_evaluation`, {method: 'POST', headers: {'Content-type': 'application/x-www-form-urlencoded; charset=;UTF-8'}, data: formData});
}


/**
 *导出题库：GET exportQuestions?id=xxx&_optype=export 加上_optype就是导出excel了
 */
export function exportQuestions(id: number) {
    return `http://192.168.110.3:5000/api/question/export_question?set_id=${id}&site=llm_evaluation&_optype=export`;
}

/**
 *删除题库
 */
export function deleteQuestions(id: number) {
    // return `http://192.168.110.3:5000/api/question/export_question?set_id=${id}&site=llm_evaluation&_optype=export`;
    const formData = new FormData();
    formData.append('set_id', id.toString());
    return request(`question_set/delete?site=llm_evaluation`, {method: 'POST', headers: {'Content-type': 'application/x-www-form-urlencoded; charset=;UTF-8'}, data: formData});
}


//////评测详情

/**
 * 创建一个评测任务
 * @param questionSetId 题库id
 * @param modelId 模型id
 * @param deadline
 * @return 评测任务的id
 */
export async function createExam(questionSetId: number, modelId: number, deadline?: string): Promise<number> {
    const formData = new URLSearchParams()
    formData.append('set_id', String(questionSetId));
    formData.append('llm_model_id', String(modelId));
    const res = await request(`exam/add?site=llm_evaluation`, {method: 'POST', headers: {'Content-type': 'application/x-www-form-urlencoded; charset=;UTF-8'}, data: formData});
    return res.data.id as unknown as number;
}

/*
* 评测任务对象的格式
* */
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

let examItemCache: examItem | null = null

/**
 * 获取一个评测任务详情
 * @param id 评测任务的id
 * @return {} 评测任务的详情，会为null
 */
export async function examDetail(id: number): Promise<examItem | null> {
    const res = await request(`exam/detail?site=llm_evaluation&exam_id=${id}`);
    examItemCache = res.data as unknown as examItem;
    return examItemCache;
}

/**
 * 提交某道题的评分：POST submitScore，
 * 参数exam_detail_id=评测详情id, submit_score=分数0~10, submit_remark=备注, submit_timecost=评测花费时间（前端自动计算，即这道题他打分花了多少时间，单位毫秒）
 * @param exam_detail_id 评测任务的id
 * @param submit_score 评测任务的分数
 * @param submit_timecost 评测任务花费的时间
 * @param submit_remark 评测任务的备注
 * @returns
 */
export function submitScore(exam_detail_id: number, submit_score: number, submit_timecost: number, submit_remark?: string) {
    if (!submit_remark) {
        submit_remark = '';
    }
    const formData = new FormData();
    formData.append('exam_detail_id', exam_detail_id.toString());
    formData.append('submit_score', submit_score);
    formData.append('submit_remark', submit_remark);
    formData.append('submit_timecost', submit_timecost.toString());
    return request(`exam_detail/submit_score?site=llm_evaluation`, {
        method: 'POST',
        headers: {'Content-type': 'application/x-www-form-urlencoded; charset=;UTF-8'},
        data: formData
    })
}

interface examListOption {
    page_num?: number,
    page_size?: number,
    llm_model_id?: number,
    create_user_id?: number,
    created_time_min?: number,
    created_time_max?: number
}

/*
* 获取评测任务列表
*/
export async function examList(option: examListOption) {
    return request(`exam/list?site=llm_evaluation&page_num=${option?.page_num}&page_size=${option?.page_size}&llm_model_id=${option?.llm_model_id}&create_user_id=${option?.create_user_id}&created_time_min=${option?.created_time_min}&created_time_max=${option?.created_time_max}`)
}

/**
 * 生成评测任务答案
 * @param exam_id 评测任务的id
 * @param question_id 问题的id
 */
export function generateAnswer(exam_id: number, question_id: number) {
    return request(`exam_detail/generate_answer?site=llm_evaluation&exam_id=${exam_id}&question_id=${question_id}`)
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
// let questionsListCache: Question[] | null = null
//
// export function questionSetDetail(id: number): Promise<Question[]> {
//     // return request(`llm_evaluation.questionSetDetail?site=llm_evaluation&id=${id}`).then(res=>{
//     return request(`question_set/detail?site=llm_evaluation&set_id=${id}`).then(res => {
//         questionsListCache = res.questions as unknown as Question[];
//         // console.info("res:", res);
//         const {code, data} = res;
//         if (code === 0) {
//             // console.info("data:", data);
//             return data.questions;
//         }
//         // console.log(questionsListCache)
//         // return questionsListCache;
//     })
// }


/**
 *  修改/新增题库：POST modifyQuestionSet，参数id、name。有id为修改题库名称，无id参数为新增题库
 * @param [id]
 * @param name
 */
// export function modifyQuestionSet(id: string | undefined, name: string) {
//     // return request(`llm_evaluation.modifyQuestionSet?site=llm_evaluation`, {method: 'POST', data: {name: name}})
//     const formData = new FormData();
//     if (typeof id === "string") {
//         formData.append('set_id', id);
//     }
//     formData.append('name', name);
//     return request(`/question_set/modify?site=llm_evaluation`, {method: 'POST', headers: {'Content-type': 'application/x-www-form-urlencoded; charset=;UTF-8'}, data: formData})
// }

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
    text: {
        sourceType: string;
        text: string
    };
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
