<template>
  <div class="main" src="bgForAnswer">
    <button class="backToIndex" @click="backToIndex">返回首页</button>
    <div class="container">
      <div class="content">
        <div class="thanks"></div>
        <h1 style="margin: 80px;">测评到此结束，感谢您的参与</h1>
        <div class="result">总评分：{{ averageScore.toFixed(2) }} 
          <span class="rating">     
            <span v-for="star in stars" :class="{ 'filled': star <= averageScore }" >
                <i class="fa fa-star"></i>
            </span>  
          </span>       
        </div>
        
      </div>
    </div>     
  </div>
  </template>

  
  <script lang="ts">
  import { Session } from '@/utils/storage';
  import { useRouter } from 'vue-router';
  import { nextTick, watch, reactive, toRefs } from 'vue';
  import { CircleCheck, Filter  } from '@element-plus/icons-vue';
  import { Question , examDetail} from '@/api';
  import { Filter } from 'element-plus';
  import '@fortawesome/fontawesome-free/css/all.css';
  
  export default {
    components: { CircleCheck},
    setup() {
        const router = useRouter();
        const state = reactive({
            questionGroupName: "题库名",
            questionGroups: [] as Question[],
            title: "",
            loading: false,
            questionIndex: 0,
            curQuestion: null,
            curModel: Session.get("modelName"),
            rating: 0,
            stars: [2, 4, 6, 8, 10],
            totalScore:0,
            averageScore:0,
            chosenQuestionGroup: Session.get("chosenQuestionGroup")
        });
      function backToIndex(){
        router.push("/llm/index")
      }
        function initResult(sid: string) {
            state.totalScore = state.chosenQuestionGroup.reduce((acc:any, item:any) => acc + item.score, 0);
            state.averageScore=state.totalScore/state.chosenQuestionGroup.length;
            examDetail(Session.get("examId")).then(res=>{
              console.log(res)
            })

            }

        watch(() => router.currentRoute.value.params.sid, (sid: string) => initResult(sid as string), { immediate: true });
        return {
            ...toRefs(state),
            backToIndex,
            
        };
    },
  
};

  </script>
  
  <style scoped lang="scss">
  .main {
    position: relative;
    width: 100vw;
    height: 100vh;
    background: url(@/assets/bgForAnswer.png);
    background-size: cover;
    .backToIndex{
      position: fixed;
      top: 20px;
      right:30px;
      width: 112px;
      height: 40px;
      border-radius: 3px;
      opacity: 1;
      border: 1px solid #dcdcdcff;
      background: #ffffffff;
    }
    .container {
      position: relative;
      top: 46%;
      left: 50%;
      transform: translate(-50%, -50%);
      display: flex;
      justify-content: space-around;
      align-items: center;
      width: 80%;
      height: 80%;
      // padding: 20%;
      border: none;
      // border-radius: 50px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
      background: #ffffffff;

    }
    .content {
      padding: 10%  ;
      position: relative; /* 将div元素设置为绝对定位 */
      top: 46%; /* 将div元素放置在蒙版的中心位置 */
      left: 50%; /* 将div元素放置在蒙版的中心位置 */
      transform: translate(-50%, -50%); /* 将div元素向左上方移动自身宽度和高度的一半 */
      display: flex; /* 使用flex布局 */
      flex-direction: column; /* 将子元素垂直排列 */
      justify-content: flex-start; /* 将子元素在主轴上居中对齐 */
      align-items: center; /* 将子元素在交叉轴上居中对齐 */
      width: 100%; /* 设置div元素的宽度 */
      height: 100%; /* 设置div元素的高度 */
      margin-top: 60px; 
     
      .thanks{  
        // position:absolute;
        margin: 14px;
        background: url(@/assets/check-circle.png);
        width: 76px;
        height: 76px;
    }
    .result{
      color: #000000e6;
      font-size: 36px;
      font-weight: 600;
      font-family: "PingFang SC";
      text-align: left;
      line-height: 44px;
      .rating {
        // display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 80px;
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
    }

    }


  


}
  </style>