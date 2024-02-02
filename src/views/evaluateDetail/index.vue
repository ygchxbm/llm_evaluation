<script setup lang="ts">
import {computed, onMounted, ref} from "vue";
import {examDetail, examItem, Question, questionSetDetail, submitScore} from "@/api";
import {useRoute} from "vue-router";
import '@fortawesome/fontawesome-free/css/all.css';
import router from "@/router";

const route = useRoute()

const examId: number = parseInt((route.query.examId as string));
// console.info("examId:", examId)
const examItem = ref<examItem | null | object>({});
const questionBankDetail = ref<Question | null | object>({});
const progressCount = ref<number>(1);
const progressColor = ref<string>('#47a5bd');
const percentage = ref<number>(0);

const isShowContent=ref<boolean>(false)


const questions = computed(() => {
  if (!(questionBankDetail.value as Question)?.questions) {
    return []
  } else {
    percentage.value = (progressCount.value) / (questionBankDetail.value as Question)?.questions.length * 100;
    // console.info("(questionBankDetail.value as Question)?.questions:", (questionBankDetail.value as Question)?.questions)
    return (questionBankDetail.value as Question)?.questions
  }
})

const aiAnswers = computed(() => {
  if (!examItem.value.my_answers) {
    return []
  } else {
    // console.info("examItem.my_answers:", examItem.value.my_answers)
    return examItem.value.my_answers
  }
})

onMounted(init)

async function init() {
  ////获取评测详情，包含ai答案
  await examDetail(examId).then(res => {
    if (res !== null) {
      examItem.value = res
    }
  }).catch(e => {
    console.info(e)
  })
  // console.info("examItem:", examItem)

  if (examItem.value === null) return
  const questionBankId: number = (<examItem>examItem.value).question_set_id;
  await questionSetDetail(questionBankId).then(res => {
    if (res !== null) {
      questionBankDetail.value = res;
      const length = res.questions.length;
      barData.value.nextStepText = Array(length).fill('下一题');
      barData.value.scores = Array(length).fill(0);
      if (length > 0) {
        isShowContent.value=true;
        barData.value.nextStepText[length - 1] = "提交";
      } else {
        barData.value.nextStepText.push("提交");
      }
    }
  }).catch(e => {
    console.info(e)
  })
  startTime = new Date().getTime();
}

const stars = [2, 4, 6, 8, 10];
const rating = ref(0);
const remark = ref('');
let startTime: number = 0;

interface barData {
  scores: number[];
  nextStepText: string[];
}

const barData = ref<barData>({
  scores: [],
  nextStepText: [],
});

function setRating(star: number) {
  rating.value = star
  barData.value.scores[progressCount.value - 1] = star;
}

async function changeProgressCount(value: number) {
  if (progressCount.value >= 1 && progressCount.value <= questions.value?.length) {
    const timeCost = new Date().getTime() - startTime;
    startTime = new Date().getTime();
    const curAnswerId = aiAnswers.value[progressCount.value - 1].id;
    await submitScore(curAnswerId, barData.value.scores[progressCount.value - 1]*2, timeCost, remark.value).then(res => {
      console.info("res:", res)
    }).catch(e => {
      console.info(e)
    })
    if (progressCount.value === questions.value?.length) {
      const sum = barData.value.scores.reduce((val, next) => {
        return val + next*2
      }, 0)
      debugger
      let averageScore = parseFloat((sum / barData.value.scores.length).toFixed(1));
      await router.push({
        name: "EvaluateEnd",
        query: {
          score: averageScore
        }
      })
    }
  }
  if (progressCount.value + value >= 1 && progressCount.value + value <= questions.value?.length) {
    progressCount.value += value;
  }
}

function rebuild() {
  init()
  progressCount.value = 1;
}

function backHome() {
  router.push('/')
}
</script>

<template>
  <div class="evaluate-detail">
    <button class="back-home" @click="backHome">返回首页</button>
    <div class="content">
      <div class="header">
        <div class="progress">
          <el-progress :percentage="percentage" :color="progressColor" :show-text="false" :stroke-width="6"/>
        </div>
        <div class="question-bank-title">{{ (questionBankDetail as Question).name }}</div>
      </div>
      <div v-if="isShowContent" class="main">
        <div class="one-question">
          <div class="question-title">{{ questions[progressCount - 1]?.question }}</div>
          <span class="question-dimension">{{ questions[progressCount - 1]?.dimension }}</span>
          <div class="question-answer">{{ questions[progressCount - 1]?.answer }}</div>
          <div class="question-model">
            <div class="question-model-name">{{ examItem?.llm_model_name }}<span> 回答 ：</span></div>
            <div class="question-model-answer">{{ aiAnswers[progressCount - 1]?.llm_answer }}</div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="isShowContent" class="bottom-bar">
      <div class="bar-content">
        <el-button class="last-step" @click="changeProgressCount(-1)">上一题</el-button>
        <div class="score">
          <span class="score-label">评分：</span>
          <span class="score-text">{{ barData.scores[progressCount - 1]*2 }}</span>
<!--          <span class="stars" v-for="star in stars" :class="{ 'filled': star <= barData.scores[progressCount - 1] }" @click="setRating(star)">-->
<!--            <i class="fa fa-star"></i>-->
<!--          </span>-->
          <el-rate v-model="barData.scores[progressCount - 1]" clearable allow-half size="large" :colors="['#00A9CE','#00A9CE','#00A9CE']"/>
<!--          <div>{{barData}}</div>-->
        </div>
        <div class="remark">
          <el-input v-model="remark" placeholder="请输入评分备注"/>
        </div>
        <el-button class="rebuild" @click="rebuild">重新生成</el-button>
        <el-button class="next-step" @click="changeProgressCount(1)">{{ barData.nextStepText[progressCount - 1] }}</el-button>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.evaluate-detail {
  width: 100%;
  //height: 100%;
  height: 100vh;
  overflow: hidden;
  background-image: url("@/assets/bgForAnswer.png");
  background-size: cover;
  display: flex;
  flex-direction: column;
  //justify-content: center;
  align-items: center;

  .back-home {
    width: 112px;
    height: 40px;
    position: absolute;
    top: 30px;
    right: 30px;
    border: 0;
    border-radius: 3px;
    background: #00a9ce;;
    cursor: pointer;
    color: #ffffffe6;
  }

  .back-home:hover {
    //box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  }

  .content {
    width: calc(100% - 540px);
    min-width: 900px;
    height: calc(100% - 120px);
    //height: 100%;
    background: #FFFFFF;
    margin-top: 60px;

    .header {

      .progress {
        margin: 10px;
      }

      .question-bank-title {
        margin: 40px 0;
        color: #000000e6;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
        line-height: 28px;
        letter-spacing: 0.24px;
      }
    }

    .main {
      margin: 0 30px;

      .one-question {
        .question-title {
          margin-bottom: 10px;
          color: #000000e6;
          font-size: 16px;
          font-weight: bold;
          text-align: left;
          line-height: 26px;
        }

        .question-dimension {
          padding: 3px 11px;
          border-radius: 3px;
          opacity: 1;
          border: 1px solid #c6e8ef;
          background: #e8f9fd;

          color: #00a9ce;
          font-size: 12px;
          font-weight: 400;
          text-align: center;
          line-height: 20px;
        }

        .question-answer {
          margin-top: 10px;
          color: #000000e6;
          font-size: 16px;
          font-weight: 400;
          text-align: left;
          line-height: 28px;
        }

        .question-model {
          width: 100%;
          min-height: 116px;
          border: 1px dashed #d8d8d8;
          background: #ffffff;
          padding: 10px 20px;

          .question-model-name {
            color: #000000e6;
            font-size: 16px;
            font-weight: 500;
            text-align: left;
            line-height: 32px;
          }

          .question-model-answer {
            color: #000000b3;
            font-size: 14px;
            font-weight: 400;
            text-align: left;
            line-height: 22px;
          }
        }
      }
    }


  }

  .bottom-bar {
    width: 100%;
    height: 70px;
    background: #FFFFFF;
    box-shadow: 0 -6px 14px 0 #0000000a;
    display: flex;
    justify-content: center;

    .bar-content {
      width: calc(100% - 540px);
      height: 70px;
      min-width: 900px;
      display: flex;
      justify-content: space-between;
      align-items: center;

      .el-button {
        width: 112px;
        height: 40px;
        border-radius: 3px;
        opacity: 1;
        border: 1px solid #dcdcdc;
        cursor: pointer;
        //background: #ffffff;
      }

      .el-button:hover {
        //box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
      }

      .last-step {
        color: #000000e6;
        font-size: 16px;
        font-weight: 400;
        text-align: center;
        line-height: 24px;
      }

      .score {
        display: flex;
        align-items: center;


        .score-label {
          color: #000000e6;
          font-size: 18px;
          font-weight: 400;
          text-align: left;
          line-height: 40px;
        }

        .score-text {
          color: #000000e6;
          font-size: 36px;
          font-weight: 600;
          text-align: left;
          line-height: 44px;
          margin-right: 16px;
          min-width: 45px;
        }

        :deep(.el-rate__icon){
          font-size: 24px;
        }

        .stars {
          cursor: pointer;
          font-size: 24px;
          color: #ccc;
          margin-right: 6px;
        }

        .filled {
          color: #00a9ce;;
        }

      }

      .remark {

        :deep(.el-input) {
          width: 240px;
          height: 32px;
          background: #ffffff;

          .el-input__wrapper {
            box-shadow: 0 0 0 2px #dcdfe6 inset
          }

          .el-input__wrapper.is-focus {
            box-shadow: 0 0 0 2px #00a9ce inset;
          }
        }
      }

      .rebuild {
        color: #000000e6;
        font-size: 16px;
        font-weight: 400;
        text-align: center;
        line-height: 24px;
      }

      .rebuild, .last-step:hover {
        background: none;
      }

      .next-step {
        background: #00a9ce;
        color: #ffffffe6;
        font-size: 16px;
        font-weight: 400;
        text-align: center;
        line-height: 24px;
      }
    }


  }
}
</style>
