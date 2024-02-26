<script setup lang="ts">
import {ArrowRight, Search} from '@element-plus/icons-vue';
import {computed, onMounted, ref} from "vue";
import {computedAsync} from '@vueuse/core'
import {useRoute} from "vue-router";
import {examDetail, modelList, Question, questionSetDetail, questionSetList} from "@/api";

const route = useRoute();

//路由传递过来的参数
interface EvaluatedAboutId {
  modeId: number;
  queBankIdList: number[];
}

const compareData: EvaluatedAboutId[] = JSON.parse((route.query.compareData) as string);
//题目内容的关键词
const keyWord = ref<string>();

//题库的id，以及与name的映射表
let queBankIdList: number[] = [];
const queBankMap = ref<{
  [prop: number]: string
}>({});
//被选择题库的id
const selectedQueBankId = ref<number>()

//模型的id，以及与name的映射表
const modeIdList = ref<number[]>([]);
const modeIdMap = ref<{
  [prop: number]: number
}>({});

//赋值queBankIdList和modeIdList
compareData.forEach(item => {
  modeIdList.value.push(item.modeId);
  item.queBankIdList.forEach(queBankId => {
    if (!queBankIdList.includes(queBankId)) {
      queBankIdList.push(queBankId)
    }
  })
})

//排序题库，优化显示效果
queBankIdList = queBankIdList.sort((a, b) => {
  return a - b
})

//默认选择第一个题库
selectedQueBankId.value = queBankIdList[0];

//评测的id
const examIdList = ref<number[]>([]);
const examIdMap: {
  [prop: number]: {
    modeId: number,
    queBankId: number
  }
} = {}


onMounted(async () => {
  await questionSetList().then(res => {
    if (res) {
      res.forEach(item => {
        Reflect.set(queBankMap.value, item.id, item.name)
      })
    }
  }).catch(e => {
    console.info("e:", e)
  })

  await modelList().then(res => {
    if (res) {
      res.forEach(item => {
        if (modeIdList.value.includes(item.id)) {
          const tempList = JSON.parse(item.question_set_exam_id);
          if (tempList) {
            for (const queBankId in tempList) {
              if (queBankIdList.includes(parseInt(queBankId)) && tempList[queBankId].length > 0) {
                const lastEvaluateId = tempList[queBankId].reverse()[0];
                examIdList.value.push(lastEvaluateId);
                Reflect.set(examIdMap, lastEvaluateId, {
                  modeId: item.id,
                  queBankId: parseInt(queBankId)
                })
              }
            }
          }
        }
        Reflect.set(modeIdMap.value, item.id, item.name)
      })
      // console.info("examIdList:", examIdList);
      // console.info("examIdMap:", examIdMap)
    }
  }).catch(e => {
    console.info(e)
  });
})


//用作答案展示的模型id，模型在有的题库下没有作答
const answerShowModeIdList = computed<number[]>(() => {
  const result: number[] = [];
  compareData.forEach((item) => {
    if (typeof selectedQueBankId.value === 'number' && item.queBankIdList.includes(selectedQueBankId.value)) {
      const modeId = item.modeId;
      result.push(modeId)
    }
  })
  // console.info("answerShowModeIdList:", answerShowModeIdList);
  return result
})

//答案展示多选框的选择结果
const answerShowSelectOption = ref<string[]>([]);


//题目的id，以及与name的映射表
const questionIdList = computedAsync<number[]>(async () => {
  const result: number[] = [];
  if (selectedQueBankId.value || selectedQueBankId.value === 0) {
    await questionSetDetail(selectedQueBankId.value).then(res => {
      if (res && res.questions.length > 0) {
        res.questions.forEach((item, index) => {
          result.push(item.id);
          const questionIndex = index < 9 ? "0" + (index + 1) + '  ' : index + 1 + '  '
          Reflect.set(questionIdMap.value, item.id, questionIndex + item.question);
        })
      }
    }).catch(e => {
      console.info(e)
    })
  }
  return result
});
const questionIdMap = ref<{
  [prop: number]: string
}>({});


interface Question {
  id: number;
  answers: Answer[];
}

interface Answer {
  modeId: number;
  answer: string;
  result: number;
}

//所有的question
const questions = computedAsync<Question[]>(async () => {
  const result: Question[] = []
  if (modeIdList.value.length > 0 && examIdList.value.length > 0 && questionIdList.value.length > 0) {
    //加入问题
    questionIdList.value.forEach(tempQuestionId => {
      const question: Question = {
        id: tempQuestionId,
        answers: []
      }
      result.push(question)
    })

    //加入答案
    for (const tempModeId of modeIdList.value) {
      for (const examId of examIdList.value) {
        const {modeId, queBankId} = examIdMap[examId];
        if ((selectedQueBankId.value || selectedQueBankId.value === 0) && (tempModeId === modeId && selectedQueBankId.value === queBankId)) {
          await examDetail(examId).then(res => {
            if (res) {
              res.my_answers.forEach(item => {
                if (questionIdList.value.includes(item.question_id)) {
                  const answer: Answer = {
                    modeId,
                    answer: item.llm_answer,
                    result: item.submit_result
                  }
                  result.forEach(tempQuestion => {
                    if (tempQuestion.id === item.question_id) {
                      tempQuestion.answers.push(answer)
                    }
                  })
                }
              })
            }
          })
        }
      }
    }
  }
  return result
})

function filterKeyWord(questions: Question[]): Question[] {
  const result: Question[] = []
  if (questions.length > 0) {
    for (const question of questions) {
      const questionText = questionIdMap.value[question.id];
      if (!keyWord.value || questionText.includes(keyWord.value)) {
        result.push(question)
      }
    }
  } else {
    console.info("11111:", 11111)
  }
  return result
}

//根据条件筛选后的的question
const questionsAfterFilter = computed(() => {
  const result: Question[] = []
  if (Array.isArray(questions.value) && questions.value.length > 0) {
    const questionsAfterKeyWord = filterKeyWord(questions.value)
    if (answerShowSelectOption.value.length === answerShowModeIdList.value.length * 2) {
      return questionsAfterKeyWord
    } else if (answerShowSelectOption.value.length === 0) {
      return result
    } else {
      return questionsAfterKeyWord.filter(question => {
        let isFlag = true;
        for (const answer of question.answers) {
          const {modeId, result} = answer;
          let str;
          if (result === 1) {
            str = "-selectTrue"
          } else if (result === -1) {
            str = "-selectFalse"
          } else {
            // str = "-"
            str = "-selectFalse"
          }

          const tempRes = modeId.toString() + str;
          if (!answerShowSelectOption.value.includes(tempRes)) {
            isFlag = false
            break
          }
        }
        return isFlag
      })
    }
  }
})
</script>

<template>
  <div class="model-details">
    <div class="breadcrumb">
      <el-breadcrumb :separator-icon="(ArrowRight as string)">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>模型对比</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="content">
      <div class="search">
        <div class="label">搜索</div>
        <div>
          <el-input
              v-model="keyWord"
              class="w-50 m-2"
              size="small"
              placeholder="请输入关键词"
              :suffix-icon="(Search as string)"
          />
          <!--          <div>{{ questions }}</div>-->
        </div>
      </div>
      <div class="tabs">
        <el-tabs v-model="selectedQueBankId" class="demo-tabs">
          <el-tab-pane v-for="id in queBankIdList" :name="id">
            <template #label>
              <span>{{ queBankMap[id] }}</span>
            </template>
          </el-tab-pane>
        </el-tabs>
      </div>
      <div class="answer-presentation">
        <div class="label">答案展示：</div>
        <div class="checkboxes">
          <div class="checkbox-group" v-for="id in answerShowModeIdList">
            <el-checkbox-group class="checkbox-label" v-model="answerShowSelectOption" :key="id">
              <span>{{ modeIdMap[id] }} :</span>
              <el-checkbox class="checkbox" :label="id+'-selectTrue'" checked>{{ '对' }}</el-checkbox>
              <el-checkbox class="checkbox" :label="id+'-selectFalse'" checked>{{ '错' }}</el-checkbox>
            </el-checkbox-group>
          </div>
        </div>
      </div>
      <div class="showDetails">
        <div class="detail" v-for="question in (questionsAfterFilter as Question[])">
          <div class="title">{{ questionIdMap[question.id] }}</div>
          <div class="texts">
            <div class="item" :class="{'item_false':answer.result===-1}" v-for="answer in question.answers">
              <div class="item-title">
                <div class="mode">{{ modeIdMap[answer.modeId] }}</div>
                <div class="logo" :class="{'logo_false':answer.result===-1}">{{ answer.result === -1 ? "x" : "√" }}</div>
              </div>
              <div class="text">{{ answer.answer }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.model-details {
  --next-bg-main-color: none;
  height: 100%;
  overflow: hidden;

  .breadcrumb {
    height: 50px;
    margin-left: 20px;
    display: flex;
    align-items: center;

    :deep(.el-breadcrumb__inner.is-link) {
      color: #00000066;
      font-size: 14px;
      font-style: normal;
      font-weight: 400;
      line-height: 22px;
    }

    :deep(.el-breadcrumb__inner.is-link):hover {
      color: #00a9ce;
    }

    :deep(.el-breadcrumb__inner) {
      color: #000000e6;
      font-size: 14px;
      font-style: normal;
      font-weight: 600;
      line-height: 22px;
    }
  }

  .content {
    width: calc(100% - 40px);
    height: 100%;
    margin: 0 20px;
    border-radius: 15px;
    background: #FFFFFF;
    overflow-y: scroll;

    .search {
      display: flex;
      margin: 16px 0 24px 37px;
      align-items: center;

      .label {
        margin-right: 16px;
        color: #000000e6;
        text-align: right;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: 22px;
      }

      :deep(.el-input__wrapper) {
        padding: 5px 12px 5px 8px;
        width: 280px;
        height: 22px;
        box-sizing: content-box;
      }

      :deep(.el-input__inner) {
        display: flex;
        height: 22px;
        flex-direction: column;
        justify-content: center;
        flex: 1 0 0;
        overflow: hidden;
        color: #00000066;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: 22px;
      }

      :deep(.el-input__wrapper.is-focus) {
        box-shadow: 0 0 0 1px #00a9ce inset;
      }
    }

    .tabs {
      margin: 0 30px;
      box-sizing: border-box;

      :deep(.el-tabs__header.is-top) {
        margin: 0;
      }

      :deep(.el-tabs__nav.is-top) {
        height: 48px;
      }

      :deep(.el-tabs__active-bar.is-top) {
      //width: 80px; height: 3px; flex-shrink: 0; background: #00A9CE;
      }

      :deep(.el-tabs__item.is-top) {
        color: #000000e6;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: 40px;
        cursor: pointer;
      }

      :deep(.el-tabs__item.is-top.is-active) {
        color: #00a9ce;
        font-size: 14px;
        font-style: normal;
        font-weight: 500;
        line-height: 40px;
      }

      :deep(.el-tabs__nav-wrap::after) {
        height: 2px !important;
      }
    }

    .answer-presentation {
      display: flex;
      margin: 20px 0 20px 30px;
      align-items: center;
      font-size: 14px;

      .label {

      }

      .checkboxes {
        display: flex;

        .checkbox-group {
          display: flex;
          align-items: center;
          min-width: 220px;
          height: 44px;
          flex-shrink: 0;
          border-radius: 6px;
          border: 1px solid #E7E7E7;
          background: linear-gradient(180deg, #FFF 0%, #F8F8F8 100%);
          box-shadow: 0 2px 2px 0 #00000005;
          margin-right: 20px;

          .checkbox-label {
            margin: 0 16px;
            color: #000000e6;
            text-align: right;
            font-size: 14px;
            font-style: normal;
            font-weight: 400;
            line-height: 22px;
            display: flex;
          }

          span {
            margin-right: 16px;
          }

          .checkbox {
            width: 38px;
            margin-right: 15px;
            color: #000000e6;
            font-size: 14px;
            font-style: normal;
            font-weight: 400;
            line-height: 22px;
            box-sizing: content-box;
          }

          :deep(.el-checkbox__label) {
            font-size: 14px;
            font-style: normal;
            font-weight: 400;
            line-height: 22px;
          }

          :deep(.el-checkbox__input .el-checkbox__inner) {
            width: 14px;
            height: 14px;
          }

          :deep(.el-checkbox__input.is-checked .el-checkbox__inner ) {
            background-color: #48aacb; /* 设置选中状态的背景颜色为红色 */
            border-color: #48aacb; /* 设置选中状态的边框颜色为红色 */

          }

          :deep(.el-checkbox__input.is-checked+.el-checkbox__label) {
            color: #000000E6;
          }
        }
      }
    }

    .showDetails {
      margin: 0 30px 60px 30px;

      .detail {
        display: flex;
        flex-direction: column;
        margin-top: 30px;

        .title {
          color: #000000e6;
          font-size: 14px;
          font-style: normal;
          font-weight: 500;
          line-height: 22px;
          margin-bottom: 20px;
        }

        .texts {
          display: flex;
          gap: 0 20px;

          .item {
            flex: 1;
            min-height: 270px;
            flex-shrink: 0;
            border-radius: 8px;
            border: 1px solid #BCEBDC;
            background: #E8F8F2;

            .item-title {
              display: flex;
              justify-content: space-between;
              margin: 20px 20px 0 20px;

              .mode {
                color: #000000e6;
                font-size: 16px;
                font-style: normal;
                font-weight: 500;
                line-height: 22px;
              }

              .logo {
                width: 22px;
                height: 22px;
                border-radius: 11px;
                background: #00A870;
                text-align: center;
                color: #FFFFFF;
                line-height: 20px;
              //cursor: pointer;
              }

              .logo_false {
                background: #E34D59FF;
              }
            }

            .text {
              flex-shrink: 0;
              color: #000000b3;
              font-size: 14px;
              font-style: normal;
              font-weight: 500;
              line-height: 24px;
              margin: 11px 20px 30px 20px;
            }
          }

          .item_false {
            background: #F9D7D9FF;
            border-color: #F9D7D9FF;
          }
        }

      }


    }
  }
}
</style>
