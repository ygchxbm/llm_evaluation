<template>
  
    <div class="main" src="bgForAnswer">
      <!-- <div class="askForHelp" @mouseenter="onHelpEnterLeave(true)" @mouseleave="onAsideEnterLeave(false)"> -->
      <div class="askForHelp" >

        <div class="dialog">
          如果模型生成答案为空说明答案加载未完成，请稍后刷新重试
    </div>
      </div>  
      <div class="container">
      <div class="content">
        <div class="progress-bar">
          <div class="progress" :style="{ width: progress + '%' }"></div>
        </div>
        <div class="questionGroupName">题库名：{{ questionGroupName }} 模型名：{{ curModel }}</div>
        <div class="questionBlock">
          <div class="questionName">{{ curQuestion.id ??loading}} {{ curQuestion.question }}</div>
          <div class="questionDimension">{{ curQuestion.dimension }}</div>

          <div class="questionReference" >模型生成答案：{{ llmAnswer }}</div>
          <div class="standardQuestion"> 标准答案：{{ curQuestion.answer }}</div>
          <div class="questionReferenceModel">其他模型生成的答案：</div>
        </div>
      </div>
    </div>  
    
      <div class="footer">
          <button v-if="questionIndex>0" class="backwardQuestion" @click="backwardQuestion()">上一题</button>
          <button v-else class="backwardQuestion" @click="backToIndex()">上一题</button>
        <span class="rating">
          <span v-for="star in stars" :class="{ 'filled': star <= rating }" @click="setRating(star)">
            <i class="fa fa-star"></i>
          </span> 
        </span>

        <button  class="backwardQuestion" @click="regenerateAnswer()">重新生成</button>
        <input class="submitRemark" placeholder="输入评分备注" v-model="submitRemark">
        <button v-if="progress<100" class="forwardQuestion" @click="forwardQuestion()">下一题</button>
        <button v-else class="submitAnswer" @click="submitAnswer()">提交</button> 
      </div>  
</div>
  </template> 
  
  <script lang="ts">
  import bgForAnswer from '@/assets/bgForAnswer.png'
  import { Session } from '@/utils/storage';
  import { useRouter } from 'vue-router';
  import { nextTick, watch, reactive, toRefs, onMounted,watchEffect } from 'vue';
  import { QuestionFilled } from '@element-plus/icons-vue';
  import { Question ,questionList, examDetail, examItem,generateAnswer, answerDetailItem, submitScore} from '@/api';
  import { stat } from 'fs';
  import '@fortawesome/fontawesome-free/css/all.css';
import { number } from 'echarts';
import { dateEquals } from 'element-plus';
import { createDecipheriv } from 'crypto';
  export default {
    name: 'chat',
	  components: {  Lock,QuestionFilled },
    setup(){
      const router = useRouter();
      // const timer = setInterval(initQuestionList, 5000);
		  const state = reactive({
        questionGroupName:Session.get("curQuestion"),
        questionGroups:[] as Question[],
        title: '',
        totalLength:0,
        loading: false,
        questionIndex:0,
        curQuestion:[] as unknown as Question,
        llmAnswer:null as unknown as string,
        submitRemark:null as unknown as string,
        curAnswer:[] as unknown as answerDetailItem,
        examItem:null as unknown as examItem,
        examId:Session.get("examId"),
        curModel:Session.get("modelName"),
        startTime:0,
        finishTime:0,
        rating: 0,
        stars: [2, 4, 6, 8, 10],
        progress: 0,
        chosenQuestionGroup:Session.get("chosenQuestionGroup")

		});

        function setRating(star:number) {
          state.rating = star;
        }
        function backToIndex(){
          router.push("questionnaire");
        }
        function regenerateAnswer(){
          console.log("it is "+state.examId+state.curQuestion.id)
					generateAnswer(state.examId,state.curQuestion.id).then(res=>{
            location.reload();
          })
        }
        function backwardQuestion(){
          state.chosenQuestionGroup[state.questionIndex].score=state.rating;
          state.questionIndex=state.questionIndex-1;
          state.curQuestion=state.chosenQuestionGroup[state.questionIndex];
          state.rating=state.chosenQuestionGroup[state.questionIndex].score
          state.progress = ((state.questionIndex+1) / state.chosenQuestionGroup.length) * 100;
        }
        function forwardQuestion(){
          if(state.rating===0||state.rating==null){
            alert("请选择分数")
          }else{
            let now = new Date();
            state.finishTime= now.getTime();
            state.curAnswer=state.examItem.my_answers[state.questionIndex];
            submitScore(state.curAnswer.id,state.rating,state.finishTime-state.startTime,state.submitRemark).then(res=>{
            state.startTime=now.getTime();
            state.chosenQuestionGroup[state.questionIndex].score=state.rating;
            state.questionIndex=state.questionIndex+1;
            state.rating=state.chosenQuestionGroup[state.questionIndex].score;
            state.curQuestion=state.chosenQuestionGroup[state.questionIndex];
            state.curAnswer=state.examItem.my_answers[state.questionIndex];
            state.llmAnswer=state.curAnswer.llm_answer
            state.progress = ((state.questionIndex+1)/state.totalLength) * 100;
          })
          }
       
        }
        function submitAnswer(){
          if(state.rating===0||state.rating==null){
            alert("请选择分数")
          }else{
          let now = new Date();
          state.finishTime= now.getTime();
          submitScore(state.curAnswer.id,state.rating,state.finishTime-state.startTime,state.submitRemark).then(res=>{
            state.chosenQuestionGroup[state.questionIndex].score=state.rating;
            Session.set("chosenQuestionGroup",state.chosenQuestionGroup);
            router.push("evaluatedPage")
          })
        }

        }
        onMounted(async()=>{
          state.examId=Session.get("examId")
          state.llmAnswer='模型生成答案未加载完毕，请稍后刷新重试'
          let data= await examDetail(state.examId)
          if(data.my_answers==null||data.my_answers==undefined){
            location.reload();
          }else{
            state.examItem=data
            console.log(state.examItem)
            state.curQuestion=state.chosenQuestionGroup[state.questionIndex];
            state.curAnswer=state.examItem.my_answers[state.questionIndex];
            state.llmAnswer=state.curAnswer.llm_answer
            state.totalLength=state.chosenQuestionGroup.length
            state.progress = ((state.questionIndex+1) / state.totalLength) * 100;
            const now = new Date();
            state.startTime=now.getTime();
          }

            
 
          })
        // function initQuestionList(){
        //   state.examId=Session.get("examId")
        //   state.llmAnswer='模型生成答案未加载完毕，请稍后刷新重试'
        //   examDetail(state.examId).then(data=>{
        //     if(data.id){
        //       state.examItem=data
        //       console.log(state.examItem)
        //       state.curQuestion=state.chosenQuestionGroup[state.questionIndex];
        //       state.curAnswer=state.examItem.my_answers[state.questionIndex];
        //       state.llmAnswer=state.curAnswer.llm_answer
        //       state.totalLength=state.chosenQuestionGroup.length
        //       state.progress = ((state.questionIndex+1) / state.totalLength) * 100;
        //       const now = new Date();
        //       state.startTime=now.getTime();
        //       clearInterval(timer);
        //     }else{

        //     }
   
        //   }).catch(e=>{
				//     console.log("在获得评测详情的时候出现错误"+e);
			  //   });

		// }
    // watch(() => router.currentRoute.value.params.sid, (sid: string) => initQuestionList(), { immediate: true }); 


        return{
            ...toRefs(state),
            setRating,
            backToIndex,
            backwardQuestion,
            forwardQuestion,
            submitAnswer,
            regenerateAnswer,
            bgForAnswer,

        }
    }
    
  };

  </script>
  
  <style scoped lang="scss">



  .main {
    position: relative;
    width: 100vw; /* 假设左边框的宽度为20px */
    height: 100vh;
    background: url(@/assets/bgForAnswer.png);
    background-size: cover;
    .askForHelp{
      color: #9a9696;
      background:url(@/assets/help-circle-filled.png);
      position: fixed;
      top: 30px;
      right: 30px;
      width: 24px;
      height: 24px;
      opacity: 1;
      z-index: 2;
      color: #ffffffff;
      font-size: 14px;
      font-weight: 400;
    }
    .dialog {
        position: absolute;
        top: 100%;
        left: 50%;
        transform: translateX(-100%);
        padding: 10px;
        background-color: #fff;
        border: 1px solid #ccc;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        display: none;
      }
      .askForHelp:hover .dialog {
        display: block;
        width: 198px;
        height: 76px;
        border-radius: 6px;
        opacity: 1;
        background: #717c94ff;
      }

    .container {
      display: flex;
      margin-top: 30px;
      position: relative;
      width: 80%;
      margin: 0 auto;
      
    }
    .content {
      position: relative;
      min-width: 100%;
      justify-content: center;
      z-index: 1;
      background-color: #fff;
      padding: 20px;
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
    
    .progress-bar{
      height: 10px;
      width: 100%;
      background-color: #f2f2f2ff;
      margin-top: 20px;

    }      
    .progress {
      height: 100%;
      width: 90%;
      background-color: #00A9CE;
      }
      .questionGroupName{
        margin: 120px; /* 设置子元素之间的间距 */
        width:auto;
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
      .questionBlock{
        .questionName{
          margin: 8px;
          height: 26px;
          opacity: 1;
          color: #000000e6;
          font-size: 16px;
          font-weight: 500;
          font-family: "PingFang SC";
          text-align: left;
        }
        .questionDimension{
          margin: 8px;
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
        .questionReference{
          margin: 23px;
          opacity: 1;
          color: #000000e6;
          font-size: 16px;
          font-weight: 400;
          font-family: "PingFang SC";
          text-align: left;
          line-height: 28px;
        }
        .standardQuestion{
          margin:10px;
          opacity: 1;
          border: 1px solid #f8b9beff;
          background: #fff5f7ff;
          color: #000000b3;
          padding: 20px;
          font-size: 16px;
          font-weight: 400;
          text-align: justify;
          line-height: 28px;
          font-family: "PingFang SC";
        }
        .questionReferenceModel{
          padding: 20px;
          margin: 10px;
          opacity: 1;
          border: 1px solid #d8d8d8ff;
          background: #ffffffff;
          color: #000000b3;
          font-size: 14px;
          font-weight: 400;
          font-family: "PingFang SC";
          text-align: left;
          line-height: 22px;
        }
      }
      .footer{
        z-index: 2;
        position: absolute;
        flex-direction:row;
        width: 100%;
        // height:70px;
        padding: 23px;
        bottom:0px;
        justify-content: center;
        background: #ffffffff;
        .backwardQuestion{
          margin-left: 300px;
          width: 112px;
          height: 40px;
          border-radius: 3px;
          opacity: 1;
          border: 1px solid #dcdcdcff;
          background: #ffffffff;
        }
        .rating {
          // display: flex; 
          justify-content: center;
          align-items: center;
          margin-left: 60px;

        }
        .rating span {
            cursor: pointer;
            font-size: 30px;
            color: #ccc;
            margin-right: 10px;
          }
          
        .rating span.filled {
          color: #ff9800;
        }
        .submitRemark{
          width: 200px; 
          margin-left: 20px;
        }
        .forwardQuestion{
          margin-left: 30px;
          // justify-content: flex-end;
          width: 96px;
          height: 40px;
          border-radius: 3px;
          opacity: 1;
          background: #00a9ceff;
          
        }

        .submitAnswer{
          margin-left: 30px;
          width: 96px;
          height: 40px;
          border-radius: 3px;
          opacity: 1;
          background: #00a9ceff;
        }
      }
  }
  </style>