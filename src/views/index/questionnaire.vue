<template>
    <div class="main">
       <div class="head">
		<Breadcrumb />
        <el-button type="primary" class="create-btn" @click="backToIndex()">Pause Answering</el-button>
       </div>
		<div class="background" ></div>
		<div class="content">
			<h1 class="pageName">{{ evaluatingModel }}模型 {{ questionGroup }}题库</h1>
			<div v-for="questionItem in questionGroups" class="questionGroupList">
				<div class="questionName">{{ questionItem.id }} {{ questionItem.question }}</div>
				<div class="questionDimension">{{ questionItem.dimension }}</div>
				<div class="referenceAnswer">{{ questionItem.standard_answer }}</div>
			</div>
		</div>
	<button class="backToIndex" @click="backToIndex()">上一步</button>
	<button class="evaluationStart" @click="evaluating()">下一步</button>
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
import { Npc, npcList, npcDetail, chat, Message, FileTuneDataType, exportFineTune, importFineTune, saveNpc, deleteNpc, Question ,questionList} from '@/api';
import Breadcrumb from '@/layout/component/breadcrumb.vue';

export default {
	name: 'chat',
	components: { Plus, DocumentCopy, ChatDotRound, Lock,Breadcrumb },
	setup() {
		const router = useRouter();
		const state = reactive({
			questionGroups:[] as Question[],
			title: '',
			loading: false,
			curQuestion:null,
			curModel:null,
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
		let cacheSid = '';
        function backToIndex(){
            router.push("/transit")
        }
		function evaluating(){
			router.push("/answering")
		}
		function initQuestionList(sid:string){
			state.loading=true;
			state.title = '发起评测';
			cacheSid = sid;
			
			// questionList().then(res => {

				// if(sid === 'all') {
					state.questionGroups= [{id:1,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱吱" ,score:0}
					,{id:2,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目", standard_answer:"" ,score:0},{id:3,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},{id:4,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},{id:5,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},{id:6,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},{id:7,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0},{id:8,dimension:"play",question:"这里是题目这里是题目这里是题目这里是题目这里是题目",standard_answer:"参考答案：这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。这里是模型生成的答案，这里是模型生成的答案。" ,score:0}];
					Session.set("chosenQuestionGroup",state.questionGroups)
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
        // function findModelAnswer(){
        //     for(const questionItem of questionGroup){
                
        //     }
        // }
		watch(() => router.currentRoute.value.params.sid, (sid: string) => initQuestionList(sid as string), { immediate: true });
        return{
            ...toRefs(state),
            backToIndex,
			evaluating,
            
        }

    
    }
}
</script>

<style scoped lang="scss">
	.main {
		position: relative;
		width: calc(100vw - 270px); /* 假设左边框的宽度为20px */
		flex-grow: 1;
		background: #f8f8f8ff;
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
	// .background {
	// 	// margin-left: 100px;
	// 	// margin-top: 30px;
	// 	// position: relative;
	// 	// width: 80%;
	// 	// margin: 0 auto;
		
	// 	// position: relative;
	// 	// top: 46%;
  	// 	// left: 50%;
	// 	// transform: translate(-50%, -50%);
	// 	// display: flex;
	// 	// justify-content: space-around;
	// 	// align-items: center;
	// 	// width: 80%;
	// 	// height: 90%;
	// 	// // padding: 20%;
	// 	// border: none;
	// 	// border-radius: 50px;
	// 	// box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
	// }
	.content{
		// position: absolute; 
		// top: 46%; 
		// left: 50%; 
		// transform: translate(-50%, -50%); 
		// display: flex; 
		// flex-direction: column; 
		// justify-content: flex-start; 
		// align-items: left; 
		// width: 70%; 
		// height: 90%; 
		// margin-top: 60px; 
		// margin-left: 30px;
		width: 80%;
		position: relative;
		justify-content: center;
		z-index: 1;
		background-color: #fff;
		padding: 20px;
		margin-left: 10%;
		margin-top: 30px;
		.pageName{
			margin: 60px; 
			text-align: center;
			line-height: 28px;
			letter-spacing: 0.24px;
			font-size: 28px;
 			font-weight: 400;
			// background: #00a9ceff;
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
	.backToIndex{
		width: 112px;
		height: 40px;
		border-radius: 3px;
		opacity: 1;
		border: 1px solid #dcdcdcff;
		background: #ffffffff;
		position: fixed;
		bottom: 80px;
		right: 28px;
		z-index: 9999;
	}
	.evaluationStart{
		width: 112px;
		height: 40px;
		border-radius: 3px;
		opacity: 1;
		background: #00a9ceff;
		position: fixed;
		bottom: 20px;
		right: 28px;
		z-index: 9999;
	}


}
</style>