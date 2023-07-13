
<template>
    <div class="main">
       <div class="head">
		<Breadcrumb />
        <el-button type="primary" class="create-btn" @click="backToIndex()">Pause Answering</el-button>
       </div>
		<div class="background" ></div>
		<div class="content">
			<h1 class="pageName">发起测评</h1>
			<div class="modelSelection">模型选择      <select class="optionClass"><option v-for="model in allModel" :value=curModel >{{ curModel=model }}</option> </select> </div>
			<div class="questionSelection">题库选择       <select class="optionClass"><option v-for="question in allQuestionGroups" :value=curQuestionGroup >{{ curQuestionGroup=question }}</option> </select></div>
			<button class="evaluationStart" @click="startEvaluation()">下一步</button>
		</div>
			
		
	</div>
</template>


<script lang="ts">
import { nextTick, watch, reactive, toRefs } from 'vue';
import { ElMessageBox, ElMessage, genFileId } from 'element-plus';
import type { UploadInstance, UploadProps, UploadRawFile, UploadUserFile } from 'element-plus'
import { useRouter } from 'vue-router';
import { Plus, DocumentCopy, ChatDotRound, Lock } from '@element-plus/icons-vue';
import useClipboard from 'vue-clipboard3';
import { setTitle } from '@/utils/other';
import { Session } from '@/utils/storage';
import Breadcrumb from '@/layout/component/breadcrumb.vue';
import { Npc, npcList, npcDetail, chat, Message, FileTuneDataType, exportFineTune, importFineTune, saveNpc, deleteNpc, Question ,questionList} from '@/api';


export default {
	name: 'choose',
	components: { Plus, DocumentCopy, ChatDotRound, Lock,Breadcrumb },
	setup() {

		const router = useRouter();
		const state = reactive({
			questionGroups:[] as Question[][],
			title: '',
			loading: false,
			allQuestionGroups:[] as string[],
			allModel:[] as string[],
			curModel:null,
			curQuestionGroup:null,
            questionGroup:Session.get("curQuestion"),
            evaluatingModel:Session.get("modelName"),
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
        function backToIndex(){
            router.push("/401")
        }
        // function findModelAnswer(){
        //     for(const questionItem of questionGroup){
                
        //     }
        // }
        function startEvaluation(){
       
            if(state.curModel&&state.curQuestionGroup){
                Session.set("curQuestion",state.curQuestionGroup)
                Session.set("modelName",state.curModel)
                router.push("/questionnaire")
            }else{
                alert("请选择模型和题库");
            }
    
        }
        function initQuestionList(sid:string){
			state.loading=true;
			state.title =  "发起评测" ;
			cacheSid = sid;
			
			// questionList().then(res => {

				// if(sid === 'all') {
					state.allModel= ["请选择","gpt3.0", "gpt4.0"];
					state.allQuestionGroups = ["请选择","group1","group2"];
					setTitle(state.title);
				// } else if(sid === 'tree') {
					
				// 	setTitle(state.title);
				// } 
				
				state.loading = false;
			// }).catch(e => {
			// 	state.loading = false;
			// 	console.error('npcList err', e);
			// 	ElMessageBox.alert(`${e}`);
			// })
		}
        watch(() => router.currentRoute.value.params.sid, (sid: string) => initQuestionList(sid as string), { immediate: true });
        return{
            ...toRefs(state),
			startEvaluation,
            backToIndex,
            
        }

    
    }
}
</script>

<style scoped lang="scss">
	.main {
		position: relative;
		width: calc(100vw - 270px); /* 假设左边框的宽度为20px */
  		height: 100vh;
		background: #f8f8f8ff;
	}
	.head {
		position: relative;
		display: flex;
		justify-content: flex-end;
		.title {
			color: #263131ff;
			font-size: 24px;
			font-weight: 600;
			padding-left: 15px;
		}
		.create-btn {
			margin-top: 20px;
			margin-right: 20px;
			width: 112px;
			height: 40px;
			border-radius: 3px;
			opacity: 1;
			background: #00a9ceff;
		}
	}
	.background {
		position: relative;
		top: 46%;
  		left: 50%;
		transform: translate(-50%, -50%);
		display: flex;
		justify-content: space-around;
		align-items: center;
		width: 95%;
		height: 90%;
		// padding: 20%;
		border: none;
		border-radius: 50px;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
	}
	.content{
		
		position: absolute; /* 将div元素设置为绝对定位 */
		top: 50%; /* 将div元素放置在蒙版的中心位置 */
		left: 50%; /* 将div元素放置在蒙版的中心位置 */
		transform: translate(-50%, -50%); /* 将div元素向左上方移动自身宽度和高度的一半 */
		display: flex; /* 使用flex布局 */
		flex-direction: column; /* 将子元素垂直排列 */
		justify-content: flex-start; /* 将子元素在主轴上居中对齐 */
		align-items: center; /* 将子元素在交叉轴上居中对齐 */
		width: 100%; /* 设置div元素的宽度 */
		height: 100%; /* 设置div元素的高度 */
		margin-top: 60px; 

		.pageName{
			margin: 120px; /* 设置子元素之间的间距 */
			width: 97px;
			height: 28px;
			opacity: 1;
			color: #000000e6;
			font-size: 24px;
			font-weight: 500;
			font-family: "PingFang SC";
			text-align: center;
			line-height: 28px;
			letter-spacing: 0.24px;
			
		}
		.modelSelection{			
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
		.evaluationStart{
			width: 96px;
			height: 40px;
			margin: 24px; 
			
			background: #00a9ceff;
			border-radius: 3px;
			color: #ffffffe6;
			font-size: 16px;
			font-weight: 400;
			font-family: "PingFang SC";
			text-align: center;
			line-height: 24px;
		}
	}
	@keyframes van-cursor-flicker {
		from {
			opacity: 0;
		}
		50% {
			opacity: 1;
		}
		100% {
			opacity: 0;
		}
	}
</style>