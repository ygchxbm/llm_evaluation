import request from '@/utils/request';

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
    if(useCache && npcListCache) {
        return Promise.resolve(npcListCache);
    }
    if(npcListLoading) {
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

export function npcDetail(id: number): Promise<Npc> {
    return request('/oasisme_npc.npcDetail?id='+id).then(res => res as unknown as Npc);
}

export function saveNpc(npc: Npc): Promise<number> {
    return request('/oasisme_npc.saveNpc', { method: 'POST', data: { data: npc } }).then(res => res as unknown as number);
}

export function getSetting(): Promise<Setting> {
    return request('/oasisme_npc.getSetting').then(res => res as unknown as Setting);
}

export function saveSetting(setting: Setting) {
    return request('/oasisme_npc.saveSetting', { method: 'POST', data: { setting } });
}

export interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export interface MessageReply {
    text: { sourceType: string; text: string };
}

export function chat(npcId: number | string, msg: string, sessionId: string, signal?: AbortController) {
    return request('/oasisme_npc.chat', { method: 'POST', data: { npcId, msg, sessionId }, signal: signal?.signal }).then(res => res as unknown as MessageReply);
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
    return request('/oasisme_npc.importFineTune', { method: 'POST', data: formData });
}

export function uploadFile(file: File) {
    const formData = new FormData();
    formData.append('file', file);
    return request('/common.uploadFile', { method: 'POST', data: formData });
}

export function deleteNpc(id: number): Promise<boolean> {
    return request('/oasisme_npc.deleteNpc', { method: 'POST', data: { id } }).then(res => res as unknown as boolean);
}