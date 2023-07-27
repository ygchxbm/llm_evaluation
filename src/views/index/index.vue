<template>
	<div v-if="title==='index'||title==='myEvaluate'" class="main">
		<div v-if="shareSuccess" id="success-box"><span class="iconPng"></span>链接已复制到剪贴板</div>
		<div class="head">
			<el-button type="primary" class="create-btn" @click="startEvaluation()">发起评测</el-button>
		</div>
			<table class="modelGradeTable">
			<tbody >
				<tr>
      				<th class="modelNameCell">模型名称</th>
      				<th class="dimensionCell">角色扮演</th>
      				<th class="dimensionCell">标题3</th>
      				<th class="dimensionCell">标题4</th>
					<th class="dimensionCell">标题3</th>
					<th class="dimensionCell">标题2</th>
      				<th class="dimensionCell">标题3</th>
      				<th class="dimensionCell">标题4</th>
					<th class="dimensionCell">标题3</th>
      				<th class="dimensionCell">总评分</th>
      				<th v-if="title==='index'" class="judgeCell">评价</th>
					<th v-else-if="title==='myEvaluate'" class="operationCell">操作</th>
    			</tr>
				<tr v-for="(item, index) in modelGrade" :key="index">
					<th class="modelNameCell">{{ modelGrade[index].name }}</th>
					<th class="dimensionCell">{{ scoreDetail[0][index].toFixed(2) }}</th>
      				<th class="dimensionCell">0</th>
      				<th class="dimensionCell">0</th>
					<th class="dimensionCell">0</th>
					<th class="dimensionCell">0</th>
      				<th class="dimensionCell">0</th>
      				<th class="dimensionCell">0</th>
					<th class="dimensionCell">0</th>
					<th class="dimensionCell">{{ modelGrade[index].score }}</th>
					<th  v-if="!isjudging[index]&&!judgeContent[index]&&title==='index'&&!modelGrade[index].conclusion" class="judgeCell" @click="startJudge(index)"><el-icon><EditPen /></el-icon></th>
					<th v-else-if="!isjudging[index]&&modelGrade[index].conclusion&&title==='index'" class="judgeCell" @click="startJudge(index)">{{ modelGrade[index].conclusion }}</th>  
					<th v-else-if="isjudging[index]&&title==='index'"	class="judgeCell">
						<input type="text" class="inputSquare" v-model="judgeContent[index]">
						<el-button class="inputBtn" @click="saveJudge(index)">Save</el-button>
					</th>  
					<th  v-else-if="title==='myEvaluate'" class="operationCell" ><el-icon @click="shareTable(index)"><Share /></el-icon><span @click="shareTable(index)" style="margin: 0 10px;">分享</span><el-icon @click="deleteTable(index)"><Delete /></el-icon><span @click="deleteTable(index)" style="margin: 0 10px;">删除</span></th>
					<th v-else-if="isjudging[index]&&title==='index'&&!modelGrade[index].conclusion"	class="judgeCell">
						<input type="text" class="inputSquare" v-model="judgeContent[index]">
						<el-button class="inputBtn" @click="saveJudge(index)">Save</el-button>
					</th>  
					<th v-else-if="!isjudging[index]&&judgeContent[index]&&title==='index'&&modelGrade[index].conclusion" class="judgeCell" @click="startJudge(index)">{{ modelGrade[index].conclusion }}</th>  
					<th v-else-if="!isjudging[index]&&judgeContent[index]&&title==='index'&&!modelGrade[index].conclusion" class="judgeCell" @click="startJudge(index)">{{ judgeContent[index] }}</th>  
				</tr>
			</tbody>
			</table>
		
	</div>
	<div v-else class="managementMain">
        <button class="import-btn" @click="importNow()">导入题库</button>
		<button class="export-btn" @click="exportGroup()">导出题库</button>
		<div class="indexSquare">
			<span v-for="groupItem in questionGroupList" :class="{ 'active': groupItem.id===currentGroupId  }" class="indexForGroup" @click="chooseGroup(groupItem)">{{ groupItem.id }}</span>
		</div>
		<div class="content">
			<div v-if="importSuccess" id="success-box"><span class="iconPng"></span>导入成功</div>
			<div v-if="importUnsuccess" id="unsuccess-box"><span class="iconPng"></span>导入失败</div>
			<div v-if="exportUnsuccess" id="unsuccess-box"><span class="iconPng"></span>导出失败</div>
			<div v-if="exportSuccess" id="success-box"><span class="iconPng"></span>导出成功</div>
			<h1 class="pageName">题库名：{{ setName }}</h1>
			<div class="deleteGroup" @click="deleteQuestionGroup(questionItem)"><el-icon><Delete /></el-icon></div>
			<div v-for="questionItem in questionGroups" class="questionGroupList">
				<div class="questionName">{{ questionItem.id }} {{ questionItem.question }}</div>
				<div class="questionDimension">{{ questionItem.dimension }}</div>
				<div class="referenceAnswer">{{ questionItem.answer }}</div>
			</div>
		</div>
		<el-dialog width="800" style="max-width: 100%" v-model="trainVisible" :close-on-click-modal="false">
			<template #header>
				<div class="train-header">
					<div class="title">导入题库</div>
				</div>
			</template>
			<div class="train-wrap">
				<el-form label-width="130px">
					<el-upload accept=".xls,.xlsx" v-model:file-list="trainFile" class="input-upload" :limit="1" :on-exceed="handleFileExceed" :auto-upload="false" :show-file-list="false">
						<template #trigger>
							<div class="file-select">
								<div class="file-info">{{ trainFile[0] ? trainFile[0].name : 'Please upload the file' }}</div>
								<el-button class="file-btn">Select</el-button>
							</div>
						</template>
					</el-upload>
					<el-form-item label="Set Selection">
						<div class="questionSelection">题库选择<select class="optionClass" v-model="curQuestionGroup"><option v-for="questionSet in questionGroupList" :value=questionSet>{{ questionSet.name }}</option> </select></div>
					</el-form-item>
					<div class="tip" v-if="trainMode === 'replace'">Warning: You should export the old data when you choose replace mode.</div>
				</el-form>
			</div>
			<template #footer>
				<div class="train-footer">
					<el-button type="primary" class="train-btn" :disabled="!trainFile.length" @click="importGroup()">Import</el-button>
				</div>
			</template>
		</el-dialog>
	</div>

</template>

<script lang="ts">
import { nextTick, watch, reactive, toRefs } from 'vue';
import { ElMessageBox, ElMessage, genFileId } from 'element-plus';
import type { UploadInstance, UploadProps, UploadRawFile, UploadUserFile } from 'element-plus'
import { useRouter } from 'vue-router';
import { Plus, DocumentCopy, ChatDotRound, Lock, EditPen,Delete,Share } from '@element-plus/icons-vue';
import useClipboard from 'vue-clipboard3';

import { Npc, npcList, npcDetail, chat, Message, FileTuneDataType, exportFineTune, importFineTune, saveNpc,  Question ,modelList, modelItem, modifyLlmModel,questionSetList,questionSetDetail, questionSetItem,importQuestions,exportQuestions} from '@/api';
import DefaultAvatar from '@/assets/avatar.png';
import FolderIcon from '@/assets/folder.png';


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
			modelGrade:null as unknown as modelItem[],
			questionGroupList:null as unknown as questionSetItem[],
			npcGroups: [] as NpcTree[][],
			questionGroups:null as unknown as Question[],
			title: '',
			trainType: 'multiple' as FileTuneDataType,
			importSuccess:false,
			exportSuccess:false,
			importUnsuccess:false,
			exportUnsuccess:false,
			shareSuccess:false,
			isjudging:[],
			scoreDetail:[] as number[][],
			judgeContent:[],
			trainFile: [] as UploadUserFile[],
			trainVisible:false,
			trainMode: 'insert' as 'replace' | 'insert',
			isSelectedQuestion:false,
			isEvaluating:false,
			setName:null,
			curQuestion:{},
			curModel:{},
			curQuestionGroup:null as unknown as questionSetItem,
			currentGroupId:null as unknown as number,
			
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
				if(sid === 'index'||sid==='history') {
					modelList().then((data: { id: number; name: string; score: number; score_detail: string; conclusion: string; }[]) => {
					state.modelGrade= data;
					const scoreDetail1=[] as number[]
					const scoreDetail2=[] as number[]
					for (const item of data) {
						const dump = JSON.parse(item.score_detail)
						if (dump && dump['角色扮演']) {
						scoreDetail1.push(dump['角色扮演'])
						}
						else(scoreDetail1.push(0))
		
     				}
					state.scoreDetail[0]=scoreDetail1
				}).catch(e=>{
					console.log("在列出模型选择的时候出现错误"+e)
				});
				} else if(sid === 'group') {
					questionSetList().then((data:{ id:number;name:string;create_user:string; create_time:string;}[])=>{
						state.questionGroupList=data;
						questionSetDetail(state.questionGroupList[0].id).then(res=>{
							state.questionGroups= res
							console.log(state.questionGroupList)
						state.currentGroupId=state.questionGroupList[0].id
						state.setName=state.questionGroupList[0].name;
						console.log("这是第几个题库" + state.questionGroupList[0].id)
						});
						
					}).catch(e=>{
						console.log("在列出题库选择的时候出现错误"+e);
					}); 

				} 
				
				state.loading = false;

		}
		function openQuestionnaire(questionGroups:Question[]){
			state.isSelectedQuestion=true
			state.curQuestion=questionGroups
		}
		function startJudge(index){
			state.isjudging[index]=true
		}
		function saveJudge(index:number){
			modifyLlmModel(state.modelGrade[index].id,state.judgeContent[index])
			state.isjudging[index]=false
		}
		function importNow(){
			state.trainVisible=true
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
			router.push('/transit');
		}

		function shareTable(index:number){
		const currentUrl = window.location.href;
        navigator.clipboard.writeText(currentUrl)
          .then(() => {
			state.shareSuccess=true;
			let successBox = document.createElement('div');
			successBox.id = 'success-box';
			document.body.appendChild(successBox);
			setTimeout(function() {
				// successBox.remove();
				state.shareSuccess=false;
			}, 3000);
            console.log('链接已复制到剪贴板');
          })
          .catch((error) => {
            console.log('复制链接失败:', error);
          });
      
		}

		function deleteTable(index:number){
			// let index=state.questionGroupList.findIndex((group) => group === questionItem);
			state.modelGrade.splice(index,1)
		}
		async function chooseGroup(groupItem:any){
			state.currentGroupId = groupItem.id;
			state.setName=groupItem.name;
			state.questionGroups=await questionSetDetail(state.currentGroupId);

		}
		function importGroup(){
			if(state.curQuestionGroup){
				importQuestions(state.curQuestionGroup.id,state.trainFile[0].raw as File).then(res=>{
					state.importSuccess=true;
					let successBox = document.createElement('div');
					successBox.id = 'success-box';
					document.body.appendChild(successBox);
					setTimeout(function() {
						// successBox.remove();
						state.importSuccess=false;
					}, 3000);
				}).catch(e=>{
					state.importUnsuccess=true;
					let successBox = document.createElement('div');
					successBox.id = 'unsuccess-box';
					document.body.appendChild(successBox);
					setTimeout(function() {
						// successBox.remove();
						state.importUnsuccess=false;
					}, 3000);
				})
			}else{
				alert("请选择你要导入的题库")
			}
			

			
		}
		function exportGroup(){
			location.href = exportQuestions(state.currentGroupId)
			state.exportSuccess=true;
			let successBox = document.createElement('div');
			successBox.id = 'success-box';
			document.body.appendChild(successBox);
			setTimeout(function() {
				// successBox.remove();
				state.exportSuccess=false;
			}, 3000);
			

		}

		function deleteQuestionGroup(questionItem:any){
			// state.questionGroupList = state.questionGroupList.filter(item => item !== questionItem);
			let index=state.questionGroupList.findIndex((group) => group === questionItem);
			state.questionGroupList.splice(index,1)
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
			// state.curNpc = npcAll[id];
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

		
		function handleUploadSuccess(field: 'avatar' | 'poster') {
			return (url: string) => state.curNpc[field] = url
		}

		function handleUploadError(e: Error) {
			ElMessage.error(`${e}`);
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
		
			handleUploadSuccess,
			handleUploadError,

			openQuestionnaire,
			startEvaluation,
			startJudge,
			saveJudge,
			shareTable,
			deleteTable,
			chooseGroup,
			importGroup,
			exportGroup,
			deleteQuestionGroup,
			importNow,
			filters: {
				formatPrice(value:any) {
				return value.toFixed(2)
				}
			},
		}
	}
	
}

</script>

<style scoped lang="scss">
	.main {
		width: calc(100vw - 270px); /* 假设左边框的宽度为20px */
  		height: 100vh;
		background: #f8f8f8ff;
		#success-box {
			text-align: center;
			position: absolute;
			flex-direction:row;
			top: 10%;
			left: 40%;
			transform: translate(-50%, -50%);
			padding: 13px;
			width: 200px;
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
		#unsuccess-box {
			text-align: center;
			position: absolute;
			flex-direction:row;
			top: 10%;
			right:40%;
			transform: translate(-50%, -50%);
			padding: 13px;
			width: 200px;
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
	min-height: 100vh;
	flex-grow: 1;
	background: #f8f8f8ff;
	
	.import-btn{
		width: 112px;
		height: 40px;
		border-radius: 3px;
		opacity: 1;
		background: #00a9ceff;
		position: fixed;
		top: 30px;
		right: 28px;
		z-index: 9999;
	}
	.export-btn{
		width: 112px;
		height: 40px;
		border-radius: 3px;
		opacity: 1;
		background: #00a9ceff;
		position: fixed;
		top: 90px;
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
		
		// margin-top: 30px;
		top:30px;
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
	
		.train-wrap {
		text-align: center;
		padding-bottom: 120px;
		.input-upload {
			.file-select {
				display: flex;
				margin-bottom: 30px;
			}
			.file-info {
				width: 505px;
				height: 40px;
				color: rgba(0, 0, 0, 0.3);
				font-size: 16px;
				line-height: 40px;
				border-radius: 3px 0 0 3px;
				border: 1px solid #dcdcdc;
				text-align: left;
				padding: 0 12px;
				border-right: none;
			}
			.file-btn {
				height: 40px;
			}
		}
		.questionSelection{
			margin: 24px;
			border-radius: 3px;
			opacity: 1;
			text-align: center;
			color: #00000080;
			font-size: 14px;
			font-weight: 400;
			font-family: "PingFang SC";
			line-height: 22px;
			.optionClass{
				width: 330px;
				height: 32px;
				border-radius: 3px;
				opacity: 1;
				color: #00000066;
			}
	}
		.tip {
			color: #e34d59;
		}
	}		

	.train-header {
		text-align: center;
		color: rgba(0, 0, 0, 0.7);
		font-size: 14px;
		.title {
			font-size: 18px;
			font-weight: 700;
			text-align: center;
			padding: 20px 0 10px;
		}
	}
	.train-footer {
		text-align: center;
		.train-btn {
			font-size: 16px;
			font-weight: 700;
			height: 40px;
			line-height: 40px;
			padding: 0 36px;
		}
	}
}
	



</style>

