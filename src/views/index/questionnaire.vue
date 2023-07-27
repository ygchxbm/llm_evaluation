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
				<div class="referenceAnswer">{{ questionItem.answer }}</div>
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
import { questionSetDetail, Question ,questionList,createExam,examDetail,examItem,generateAnswer} from '@/api';
import Breadcrumb from '@/layout/component/breadcrumb.vue';
import { stat } from 'fs';

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
			examId:null as unknown as number,
			examItem:null as unknown as examItem,
            questionGroup:Session.get("curQuestion"),
            evaluatingModel:Session.get("modelName"),
			modelId:Session.get("modelId"),
			questionSetId:Session.get("questionnaireId")
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
			for(let i=0;i<state.examItem.question_count;i++){
						generateAnswer(state.examId,state.examItem.questions[i].id).then(res=>{
							
								router.push("/answering")
							
						})
					}	
			
		}
		function initQuestionList(sid:string){
			state.loading=true;
			state.title = '发起评测';
			cacheSid = sid;
			questionSetDetail(state.questionSetId).then((data:{ id:number;set_id:number;question:string;dimension:string;answer:string;}[])=>{
				console.log(data)
				state.questionGroups=data;
				createExam(state.questionSetId,state.modelId).then(data=>{
				state.examId =data
				console.log("exam id is " + state.examId)
				examDetail(state.examId).then(data=> {
					state.examItem=data
					Session.set("chosenQuestionGroup",state.questionGroups)
					Session.set("examId",state.examId)
					
				}).catch(e=>{
				console.log("在获得评测详情的时候出现错误"+e);
			});

			}).catch(e=>{
				console.log("在发起评测的时候出现错误"+e);

			})
			}).catch(e=>{
				console.log("在请求题库具体题目时出现错误"+e);
			});
			// console.log(state.questionGroups)
			setTitle(state.title);
			state.loading = false;
		}
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
		min-height: 100vh;
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