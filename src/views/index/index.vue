<template>
	<div v-if="title==='index'||title==='myEvaluate'" class="main">
		<div class="head">
			<el-button type="primary" class="create-btn" @click="startEvaluation()">发起评测</el-button>
		</div>
			<table class="modelGradeTable">
			<tbody >
				<tr>
      				<th class="modelNameCell">标题1</th>
      				<th class="dimensionCell">标题2</th>
      				<th class="dimensionCell">标题3</th>
      				<th class="dimensionCell">标题4</th>
					<th class="dimensionCell">标题3</th>
      				<th class="dimensionCell">总评分</th>
      				<th v-if="title==='index'" class="judgeCell">评价</th>
					<th v-else-if="title==='myEvaluate'" class="operationCell">操作</th>
    			</tr>
				<tr v-for="(item, index) in modelGrade" :key="index">
					<th v-for="(field, key) in item" :key="key" class="modelNameCell">
						<span >{{ field }}</span>
					</th>
					<th  v-if="!isjudging[index]&&!judgeContent[index]&&title==='index'" class="judgeCell" @click="startJudge(index)"><el-icon><EditPen /></el-icon></th>
					<th v-else-if="isjudging[index]&&title==='index'"	class="judgeCell">
						<input type="text" class="inputSquare" v-model="judgeContent[index]">
						<el-button class="inputBtn" @click="saveJudge(index)">Save</el-button>
					</th>  
					<th  v-else-if="title==='myEvaluate'" class="operationCell" ><el-icon @click="shareTable(index)"><Share /></el-icon><span @click="shareTable(index)" style="margin: 0 10px;">分享</span><el-icon @click="deleteTable(index)"><Delete /></el-icon><span @click="shareTable(index)" style="margin: 0 10px;">删除</span></th>
					<th v-else-if="isjudging[index]&&title==='index'"	class="judgeCell">
						<input type="text" class="inputSquare" v-model="judgeContent[index]">
						<el-button class="inputBtn" @click="saveJudge(index)">Save</el-button>
					</th>  
					<th v-else-if="!isjudging[index]&&judgeContent[index]&&title==='index'" class="judgeCell" @click="startJudge(index)">{{ judgeContent[index] }}</th>  
				</tr>
			</tbody>
			</table>
		
	</div>
	<div v-else class="managementMain">
        <button class="import-btn" @click="importGroup()">导入题库</button>
		<div class="indexSquare">
			<span v-for="groupItem in questionGroupList" :class="{ 'active': groupItem[0].id===currentGroupId  }" class="indexForGroup" @click="chooseGroup(groupItem)">{{ groupItem[0].id }}</span>
		</div>
		<div class="content">
			<div v-if="importSuccess" id="success-box"><span class="iconPng"></span>导入成功</div>
			<h1 class="pageName">模型 题库</h1>
			<div class="deleteGroup" @click="deleteQuestionGroup(questionItem)"><el-icon><Delete /></el-icon></div>
			<div v-for="questionItem in questionGroups" class="questionGroupList">
				<div class="questionName">{{ questionItem.id }} {{ questionItem.question }}</div>
				<div class="questionDimension">{{ questionItem.dimension }}</div>
				<div class="referenceAnswer">{{ questionItem.standard_answer }}</div>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import { nextTick, watch, reactive, toRefs } from 'vue';
import { ElMessageBox, ElMessage, genFileId } from 'element-plus';
import type { UploadInstance, UploadProps, UploadRawFile, UploadUserFile } from 'element-plus'
import { useRouter } from 'vue-router';
import { Plus, DocumentCopy, ChatDotRound, Lock, Minus,EditPen,Delete,Share } from '@element-plus/icons-vue';
import useClipboard from 'vue-clipboard3';
import { setTitle } from '@/utils/other';
import { Npc, npcList, npcDetail, chat, Message, FileTuneDataType, exportFineTune, importFineTune, saveNpc, deleteNpc, Question ,questionList} from '@/api';
import Npc1 from '@/assets/npc1.jpg';
import Npc2 from '@/assets/npc2.jpg';
import { Session } from '@/utils/storage';
import DefaultAvatar from '@/assets/avatar.png';
import FolderIcon from '@/assets/folder.png';
import iconPng from '@/assets/icon.png';

interface NpcTree extends Npc {
	parents: string[];
	parentIds: number[];
	children: NpcTree[];
}
interface QuestionTree extends Question{
	parents:string[];
	parentIds:number[];
	children:QuestionTree[]
}

export default {
	name: 'Chat',
	components: { Plus, DocumentCopy, ChatDotRound, Lock, EditPen, Delete,Share },
	setup() {
		const router = useRouter();
		const state = reactive({
			modelGrade:null,
			questionGroupList:null,
			npcGroups: [] as NpcTree[][],
			questionGroups:null,
			title: '',
			importSuccess:false,
			isjudging:[],
			judgeContent:[],
			isSelectedQuestion:false,
			isEvaluating:false,
			operMore: false,
			loading: false,
			filterNpc: -1,
			curNpc: { avatar: '', id: 1, name: 'Perfectionist' } as NpcTree,
			curQuestion:{},
			curModel:{},
			currentGroupId:null,
			chatVisible: false,
			userInput: '',
			userInpuHeight: 0,
			sending: 0,
			messages: [] as Message[],
			chatModel: 'default' as 'defalut' | 'gpt',
			messageInputing: -1,
			trainVisible: false,
			trainType: 'multiple' as FileTuneDataType,
			trainFile: [] as UploadUserFile[],
			training: false,
			trainMode: 'insert' as 'replace' | 'insert',
			profileVisible: false,
			profileSaving: false,
			npcAllGroup: [] as NpcTree[],
		});
		const refDoms = {
			bottomDom: null as HTMLElement | null,
			fakeInput: null as HTMLElement | null,
			trainFile: null as UploadInstance | null,
		};
		const sessionId = `${Date.now()}`;
		let sendingTimer: ReturnType<typeof setInterval>;
		let stopSignal: AbortController;
		const { toClipboard } = useClipboard();
		const npcAll: Record<number, NpcTree> = {};
		const cacheMessages: Record<number, Message[]> = {};
		let cacheSid = '';

		function addDbMessage() {
			// addMessage(nMessage).then(id => {
			// 	nMessage.id = id;
			// 	const index = session.value.messages.findIndex(x => +x.id === +id);
			// 	if(index >= 0) {
			// 		session.value.messages[index] = nMessage;
			// 	} else {
			// 		session.value.messages.push(nMessage)
			// 	}
			// }).catch(e => {
			// 	console.error('addMessage err', e);
			// })
		}

		function initQuestionList(sid:string){
			state.loading=true;
			state.title = sid === 'index' ? 'index' : (sid === 'history' ? 'myEvaluate' : 'questionGroup');
			cacheSid = sid;
			
			// questionList().then(res => {

				if(sid === 'index') {
					state.modelGrade=[{name:"gpt3.5",dimension1:2,dimension2:4,dimension3:6,dimension4:4,dimension5:5},{name:"gpt4.0",dimension1:1,dimension2:2,dimension3:3,dimension4:4,dimension5:5}]
					// state.questionGroups = [{id: 1, parent_id: 0, question: "test", dimension:"角色扮演",standard_answer: "testAnswer", reference_answer:{ model:"gpt3.0",answer:"SS" }},{id: 2, parent_id: 0, question: "test", standard_answer: "testAnswer", reference_answer: { model:"gpt4.0",answer:"ss" }}];
				} else if(sid === 'history') {
					state.modelGrade=[{name:"gpt3.5",dimension1:2,dimension2:4,dimension3:6,dimension4:4,dimension5:5},{name:"gpt4.0",dimension1:1,dimension2:2,dimension3:3,dimension4:4,dimension5:5}]
				} else if(sid === 'group') {
					state.questionGroupList= 
					[[
						{id:1,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},
						{id:2,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目", standard_answer:"" ,score:0},
						{id:3,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},
						{id:4,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},
						{id:5,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},
						{id:6,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0}
					]
					,[
						{id:1,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},
						{id:2,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目", standard_answer:"" ,score:0},
						{id:3,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},
						{id:4,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},
						{id:5,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0}
					]
					,[
						{id:1,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},
						{id:2,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目", standard_answer:"" ,score:0},
						{id:3,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},
						{id:4,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},
						
					]];
					state.questionGroups=state.questionGroupList[0];
				} 
				
				state.loading = false;
			// }).catch(e => {																
			// 	state.loading = false;
			// 	console.error('npcList err', e);
			// 	ElMessageBox.alert(`${e}`);
			// })
		}
		function openQuestionnaire(questionGroups:Question[]){
			state.isSelectedQuestion=true
			state.curQuestion=questionGroups
		}
		function startJudge(index){
			state.isjudging[index]=true
		}
		function saveJudge(index){
			state.isjudging[index]=false
		}
        function sendMessage(index: number) {
			const messageLast = state.messages.length - 1;
			sendingTimer = setInterval(() => {
				state.sending = state.sending > 2 ? 1 : state.sending + 1;
			}, 1000);
			state.messageInputing = index;
			stopSignal = new AbortController();
			const prompt = state.messages[messageLast - 1].content;
			// const msgIndex = Math.floor(messageLast / 2);
			// const startTime = Date.now();
            return chat(state.curNpc.model_id || state.curNpc.id, prompt, `${state.curNpc.id}${sessionId}`, stopSignal).then((res: { text: { text: any; }; }) => {
                state.messages[index].content = res.text ? res.text.text : 'Api Error';
				cacheMessages[state.curNpc.id] = state.messages;
				if(index === messageLast) {
					nextTick(scrollBottom);
				}
				state.messageInputing = -1;
				// const timecost = Date.now() - startTime;
				// const completion = state.messages[index].content;
				// addDbMessage({ id: 0, session_id: session.value.id, msg_index: msgIndex, prompt, completion, time_cost: timecost, score: 0, chat_id: res.id })
				clearInterval(sendingTimer);
				state.sending = 0;
                return res;
            }).catch((e: { name: string; toString: () => any; }) => {
				if(!(e instanceof DOMException && e.name == "AbortError")) {
					ElMessage.error({ message: e.toString(), duration: 0, showClose: true });
				}
                state.messageInputing = -1;
                console.error('sendMessage err', e);
				clearInterval(sendingTimer);
				state.sending = 0;
            });
		}

		function startEvaluation(){
			state.isEvaluating=true;
			router.push("/transit");
		}

		function shareTable(index:number){

		}
		function deleteTable(index:number){

		}
		function chooseGroup(groupItem:any){
			state.questionGroups=groupItem;
			state.currentGroupId = groupItem[0].id;
		}
		function importGroup(){
			state.importSuccess=true;
			let successBox = document.createElement('div');
			successBox.id = 'success-box';
			document.body.appendChild(successBox);
			setTimeout(function() {
				// successBox.remove();
				state.importSuccess=false;
			}, 3000);
			
		}

		function deleteQuestionGroup(questionItem:any){
			state.questionGroupList = state.questionGroupList.filter(item => item !== questionItem);
		}

		function addSendMessage() {
			if(!state.userInput || state.sending > 0) {
                return;
            }
			const uMessage: Message = { role: "user", content: state.userInput };
            state.messages.push(uMessage);
			nextTick(scrollBottom);
			const index = state.messages.length;
            state.messages.push({ role: 'assistant', content: '' });
            state.userInput = "";
			state.userInpuHeight = 0;
			sendMessage(index);
			state.sending = 2;
		}

		function stopSending() {
			if(stopSignal) {
				stopSignal.abort('cancel');
			}
		}

        function scrollBottom() {
            refDoms.bottomDom && refDoms.bottomDom.scrollIntoView();
        }

		function messageLiked(mindex: number, isLike: boolean) {
			// const item = session.value.messages[Math.floor(mindex/2)];
			// return item && item.score === (isLike ? 1 : -1);
		}

		function hLikeMessage(mindex: number, isLike: boolean) {
			// const item = session.value.messages[Math.floor(mindex/2)];
			// const nScore = (isLike ? 1 : -1);
			// if(item) {
			// 	item.score = +item.score === nScore ? 0 : nScore;
			// 	likeMessage(item.id, item.score);
			// }
		}

		function chatNow(id: number) {
			state.curNpc = npcAll[id];
			state.chatVisible = true;
			state.messages = cacheMessages[id] || [];
		}

		function trainNow(id: number) {
			state.curNpc = npcAll[id];
			state.trainVisible = true;
		}

		const handleFileExceed: UploadProps['onExceed'] = (files: any[]) => {
			refDoms.trainFile?.clearFiles()
			const file = files[0] as UploadRawFile
			file.uid = genFileId()
			refDoms.trainFile?.handleStart(file)
		}

		function importTrain() {
			state.training = true;
			importFineTune(state.curNpc.id, state.trainType, state.trainMode, state.trainFile[0].raw as File).then((res: any) => {
				state.training = false;
				ElMessage.success('Import success');
			}).catch((e: any) => {
				state.training = false;
				ElMessageBox.alert(`Import Failed: ${e}`);
				console.error('importFineTune error', e);
			})
		}

		function exportTrain() {
			location.href = exportFineTune(state.curNpc.id, state.trainType);
		}

		function goProfile(id: number, parentId?: number) {
			state.loading = true;
			state.profileVisible = true;
			if(id > 0) {
				npcDetail(id).then(res => {
					if(!res) {
						throw 'Null return';
					}
					state.loading = false;
					state.curNpc = { ...npcAll[id], ...res };
				}).catch(e => {
					state.loading = false;
					console.error('npcDetail err', e);
				})
			} else {
				const parentIds: number[] = parentId ? npcAll[parentId].parentIds.concat(parentId) : [];
				state.curNpc = { id: 0, parent_id: 0, name: 'New', avatar: '', poster: '', personality_data: '', world_base_knowledge: '', location_knowledge: '', parentIds, parents: [], children: [] };
			}
		}

		function handleSaveProfile() {
			const plen = state.curNpc.parentIds.length;
			state.curNpc.parent_id = plen > 0 ? state.curNpc.parentIds[plen-1] : 0;
			state.profileSaving = true;
			saveNpc({ ...state.curNpc, parentIds: undefined, parents: undefined, children: undefined } as Npc).then(() => {
				state.profileSaving = false;
				state.profileVisible = false;
				ElMessage.success('Save Success');
				window.location.reload();
			}).catch(e => {
				state.profileSaving = false;
				ElMessageBox.alert(`${e}`);
				console.error('saveNpc', e);
			})
		}

		function initNpcList(sid: string) {
			state.loading = true;
			state.title = sid === 'all' ? 'Show All' : 'Character Tree';
			cacheSid = sid;
			Object.keys(npcAll).forEach(k=>delete(npcAll[k]));
			npcList().then(res => {
				const tree: NpcTree[] = [];
				res.forEach(x => npcAll[x.id] = { ...x, parents: [], parentIds: [], children: [], poster: x.poster || (Math.random() > 0.5 ? Npc1 : Npc2) });
				res.forEach(x => {
					if(+x.parent_id === 0) {
						tree.push(npcAll[x.id]);
					} else if(npcAll[x.parent_id]) {
						npcAll[x.parent_id].children.push(npcAll[x.id]);
						npcAll[x.id].parents.push(npcAll[x.parent_id].name);
						npcAll[x.id].parentIds.push(x.parent_id);
					} else {
						console.error('not found npc', x.parent_id);
					}
				});
				const recSetParents = function(item: NpcTree, mkey: 'parents' | 'parentIds', curr: (string | number)[]) {
					if(item.parent_id > 0 && npcAll[item.parent_id]) {
						return (npcAll[item.parent_id][mkey] as (string | number)[]).concat(curr);
					}
					return curr;
				};
				Object.values(npcAll).forEach(item => {
					item.parents = recSetParents(item, 'parents', item.parents) as string[];
					item.parentIds = recSetParents(item, 'parentIds', item.parentIds) as number[];
				});
				if(sid === 'all') {
					state.npcGroups = [[], Object.values(npcAll)];
					setTitle(state.title);
				} else if(sid === 'tree') {
					state.npcGroups = [[], tree];
					setTitle(state.title);
				} else {
					state.npcGroups = [[npcAll[sid]], npcAll[sid].children];
					state.title = `${npcAll[sid].parents ? npcAll[sid].parents.join(' / ') : '' } / ${npcAll[sid].name}`;
					setTitle(npcAll[sid].name);
				}
				state.npcAllGroup = tree;
				state.loading = false;
			}).catch(e => {
				state.loading = false;
				console.error('npcList err', e);
				ElMessageBox.alert(`${e}`);
			})
		}

		function goNpc(id: number, groupIndex: number) {
			const npc = npcAll[id];
			if(groupIndex > 0 && npc.children.length > 0) {
				router.push(`/npc/${id}`);
			}
		}

		function handleUploadSuccess(field: 'avatar' | 'poster') {
			return (url: string) => state.curNpc[field] = url
		}

		function handleUploadError(e: Error) {
			ElMessage.error(`${e}`);
		}

		function handleDeleteNpc(id: number) {
			ElMessageBox.confirm('Sure to Delete?').then(() => {
				deleteNpc(id).then(() => {
					ElMessage.success('Delete Success');
					if(state.npcGroups[0][0] && state.npcGroups[0][0].id === id) {
						router.replace('/npc/all');
					} else {
						window.location.reload();
					}
				}).catch(e => {
					ElMessageBox.alert(`${e}`);
					console.error('saveNpc', e);
				})
			}).catch(()=>{});
		}

        watch(() => router.currentRoute.value.params.sid, (sid: string) => initQuestionList(sid as string), { immediate: true });
  
		return {
			...toRefs(state),
			inputMessage(e: KeyboardEvent) {
				if(!e.shiftKey && e.key === 'Enter') {
					e.preventDefault();
					addSendMessage();
				}
			},
			changeMessage() {
				nextTick(() => state.userInpuHeight = refDoms.fakeInput ? refDoms.fakeInput.scrollHeight : 0);
			},
			addSendMessage,
            sendMessage,
			stopSending,
			reSendMessage() {
				const index = state.messages.length - 1;
				state.messages[index] = { role: 'assistant', content: '' };
				sendMessage(index);
			},
			setRef(key: 'bottomDom' | 'fakeInput') {
				return (el: any) => refDoms[key] = el;
			},
			copyMessage(index: number) {
				toClipboard(state.messages[index].content).then(() => ElMessage.success('Copied'));
			},
			messageLiked,
			hLikeMessage,
			DefaultAvatar,
			chatNow,
			trainNow,
			handleFileExceed,
			exportTrain,
			importTrain,
			goProfile,
			handleSaveProfile,
			FolderIcon,
			goNpc,
			handleUploadSuccess,
			handleUploadError,
			handleDeleteNpc,
			openQuestionnaire,
			startEvaluation,
			startJudge,
			saveJudge,
			shareTable,
			deleteTable,
			chooseGroup,
			importGroup,
			deleteQuestionGroup
		}
	}
}

</script>

<style scoped lang="scss">
	.main {
		width: calc(100vw - 270px); /* 假设左边框的宽度为20px */
  		height: 100vh;
		background: #f8f8f8ff;
	}
	.head {
		
		display: flex;
		justify-content: flex-end;
		// .title {
		// 	color: #263131ff;
		// 	font-size: 24px;
		// 	font-weight: 600;
		// 	padding-left: 15px;
		// }
		.create-btn {
			margin-top: 20px;
			margin-right: 20px;
			width: 112px;
			height: 40px;
			border-radius: 3px;
			opacity: 1;
			background: #00a9ceff;
			// padding: 8px 24px;
			// height: 40px;
			// border-radius: 3px;
			// background: #36a6bf;
			// &:hover {
			// 	color: rgba(255, 255, 255, 0.9);
			// 	background: #091416;
			// }
		}
	}
	.modelGradeTable{
		justify-content: center;
		margin-top: 30px;
		border-collapse: collapse;
		display:flex;
		flex-wrap:wrap;
		.modelNameCell{
			border-bottom: 1px solid #e7e7e7ff;
			border-right: 1px solid #e7e7e7ff;
			background: #ffffffff;
			width: 200px;
			height: 46px;
			opacity: 1;
		}
		.dimensionCell{
			border-bottom: 1px solid #e7e7e7ff;
			border-right: 1px solid #e7e7e7ff;
			background: #ffffffff;
			width: 140px;
			height: 46px;
			opacity: 1;
		}
		.judgeCell{
			border-bottom: 1px solid #e7e7e7ff;
			border-right: 1px solid #e7e7e7ff;
			background: #ffffffff;
			width: 260px;
			height: 46px;
			opacity: 1;
		}
		.operationCell{
			border-bottom: 1px solid #e7e7e7ff;
			border-right: 1px solid #e7e7e7ff;
			background: #ffffffff;
			width: 260px;
			height: 46px;
			opacity: 1;
		}
		.inputSquare{
			width: 200px; 
		}
		.inputBtn{
			width: 44px;
			height: 24px;
			border-radius: 3px;
			opacity: 1;
			background: #00a9ceff;
		}
	}
	.npclist {
		display: flex;
		flex-wrap: wrap;
		.questionnaireSquare{
			width: 280px;
			height: 420px;
			border-radius: 10px;
			background: #fff;
			color: rgb(38, 49, 49);
			box-shadow: 0 4px 14px 0 rgba(38, 49, 49, 0.1);
			margin: 15px;
			padding: 10px;
			text-align: center;
			cursor: pointer;
			position: relative;
		}
		.modelSelection{
			width: 280px;
			height: 420px;
			border-radius: 10px;
			background: #140d0d;
			color: rgb(28, 140, 140);
			box-shadow: 0 4px 14px 0 rgba(38, 49, 49, 0.1);
			margin: 15px;
			padding: 10px;
			text-align: center;
			cursor: pointer;
			position: relative;
		}

	}
	.mask{
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(255, 255, 255, 0.5);
		z-index: 999;
		display: none;
		.questionnaire{
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(159, 109, 109, 0.5);
		z-index: 999;
		display: none;

	}
	}
.managementMain{
	position: relative;
	width: calc(100vw - 270px); /* 假设左边框的宽度为20px */
	flex-grow: 1;
	background: #f8f8f8ff;
	
	.import-btn{
		width: 112px;
		height: 40px;
		border-radius: 3px;
		opacity: 1;
		background: #00a9ceff;
		position: fixed;
		top: 20px;
		right: 28px;
		z-index: 9999;
	}
	.indexSquare{
		margin-top: 48px;
		margin-left: calc(10vw - 167px);
		position: fixed;
		display: flex;
		width: 140px;
		flex-direction: column;
		text-align: center;
		// border-right: 1px solid #ccc;
		.indexForGroup{
			width: 140px;
			margin: 6px;
			height: 32px;
			background: #edededff;
			border-right: 1px solid #ccc;
			
		}
		.active {
				background-color: #00A9CE;
				color: #fff;
			}
	}


	.content{
		width: 80%;
		position: relative;
		justify-content: center;
		z-index: 1;
		background-color: #fff;
		padding: 20px;
		margin-left: 10%;
		margin-top: 30px;
		#success-box {
			text-align: center;
			position: absolute;
			flex-direction:row;
			top: 10%;
			left: 40%;
			transform: translate(-50%, -50%);
			padding: 13px;
			width: 116px;
			height: 48px;
			border-radius: 6px;
			opacity: 1;
			color: #000000e6;
			font-size: 14px;
			font-weight: 400;
			border: 0.5px solid #dcdcdcff;
			background: #ffffffff;
			box-shadow: 0 6px 30px 5px #0000000d, 0 16px 24px 2px #0000000a, 0 8px 10px -5px #00000014;
			animation: fade-out 4s ease-out;
			.iconPng{
				// left: 10%;
				// display: flex;
				// position: relative;
				background: url(@/assets/icon.png);
				width: 20px;
				height: 20px;
				opacity: 1;
				
			}
		}
		@keyframes fade-out {
			100% {
					opacity: 0;
				}
				0% {
					opacity: 1;
				}

			}
		.pageName{
			margin: 60px; 
			text-align: center;
			line-height: 28px;
			letter-spacing: 0.24px;
			font-size: 28px;
 			font-weight: 400;
			// background: #00a9ceff;
		}
		.deleteGroup{
			position: absolute;
			top: 100px;
			right:50px;
		}
		.questionGroupList{
			
			.questionName{
				
				margin: 8px;
				height: 26px;
				opacity: 1;
				color: #000000e6;
				font-size: 16px;
				font-weight: 500;
				font-family: "PingFang SC";
				text-align: left;
				// line-height: 26px;
				
			}
			.questionDimension{
				width: 70px;
				height: 24px;
				border-radius: 3px;
				opacity: 1;
				border: 1px solid #c6e8efff;
				background: #e8f9fdff;
				color: #00a9ceff;
				font-size: 12px;
				font-weight: 400;
				font-family: "PingFang SC";
				text-align: center;
				line-height: 20px;
			}
			.referenceAnswer{
				margin: 20px;
				opacity: 1;
				color: #000000b3;
				font-size: 16px;
				font-weight: 400;
				font-family: "PingFang SC";
				text-align: left;
				line-height: 28px;
			}
		}


	}
	.content::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: -1;
      background: #ffffffff;
    }

}

</style>

