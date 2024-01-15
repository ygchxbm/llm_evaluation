<script setup lang="ts">
import {modelList, questionSetItem, questionSetList, modelItem, createExam, examDetail, examItem, generateAnswer} from "@/api";
import {onMounted, ref} from "vue";
import router from "@/router";
import {ElLoading} from 'element-plus'

const questionBankList = ref<questionSetItem[]>([]);
const selectedQuestionBankId = ref<number>();
const modeDataList = ref<modelItem[]>([]);
const selectedModeId = ref<number>();
const selectedEvaluationType = ref("artificial");

onMounted(async () => {
  await questionSetList().then(res => {
    questionBankList.value = res;
    // console.info("questionSetList:", res)
  }).catch(e => {
    console.info(e)
  })

  await modelList().then(res => {
    // console.info("modelList:", res)
    modeDataList.value = res;
  }).catch(e => {
    console.info(e)
  });
})

function changeEvaluationType(val: string) {
  selectedQuestionBankId.value = undefined;
  selectedModeId.value = undefined;
  selectedEvaluationType.value = val;
}

async function submit() {


  if (selectedEvaluationType.value === 'auto') {
    if (selectedQuestionBankId.value === undefined) {
      alert('请选择题库')
    } else {
      console.info("自动请求:", '自动请求')
    }
  } else if (selectedEvaluationType.value === 'artificial') {
    if (selectedQuestionBankId.value === undefined && selectedModeId.value !== undefined) {
      alert('请选择题库')
    } else if (selectedQuestionBankId.value !== undefined && selectedModeId.value === undefined) {
      alert('请选择模型')
    } else if (selectedQuestionBankId.value === undefined && selectedModeId.value === undefined) {
      alert('请选择题库和模型')
    } else {
      if (selectedQuestionBankId.value === undefined || selectedModeId.value === undefined) return

      //创建遮罩
      const loading = ElLoading.service({
        lock: true,
        text: 'Loading',
        background: 'rgba(0, 0, 0, 0.7)',
      })

      setTimeout(() => {
        loading.close();
      }, 60000)

      //创建评测任务，获取评测任务id
      let examId: number | undefined = undefined;
      await createExam(selectedQuestionBankId.value, selectedModeId.value).then(async res => {
        examId = res;
        console.info("examId:", examId)
      }).catch(e => {
        loading.close();
        console.info(e)
      })
      if (examId === undefined) return

      //获取评测详情，不含ai答案
      let examItem: examItem | null = null;
      await examDetail(examId).then(res => {
        if (res !== null) {
          examItem = res
        }
      }).catch(e => {
        loading.close();
        console.info(e)
      })
      // console.info("examItem:", examItem)
      if (examItem === null) return

      //请求ai作答，无返回
      examItem = examItem as examItem
      for (let i = 0; i < examItem.question_count; i++) {
        await generateAnswer(examId, examItem.questions[i].id);
      }

      loading.close();
      await router.push({
        name: "EvaluateDetail",
        query: {
          examId
        }
      });
    }
  }
}
</script>

<template>
  <div class="initiate-evaluation">
    <div class="content">
      <div class="title">发起测评</div>
      <div class="evaluation-type">
        <div class="evaluation-type-item" @click="changeEvaluationType('auto')" :class="{'isSelected':selectedEvaluationType==='auto'}">自动评测</div>
        <div class="evaluation-type-item" @click="changeEvaluationType('artificial')" :class="{'isSelected':selectedEvaluationType==='artificial'}">人工评测</div>
      </div>
      <div class="select-question-bank">
        <span class="label">选择题库</span>
        <el-select v-model="selectedQuestionBankId" class="m-2" placeholder="请选择" size="small">
          <el-option
              v-for="item in questionBankList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
          />
        </el-select>
      </div>
      <div class="select-model" v-if="selectedEvaluationType==='artificial'">
        <span class="label">选择模型</span>
        <el-select v-model="selectedModeId" class="m-2" placeholder="请选择" size="small">
          <el-option
              v-for="item in modeDataList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
          />
        </el-select>
      </div>
      <el-button class="submit-btn" @click="submit()">发布
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.initiate-evaluation {
  height: 100%;
  overflow: hidden;

  .content {
    margin: 20px;
    width: calc(100% - 40px);
    height: calc(100% - 40px);
    border-radius: 15px;
    background: #FFFFFF;
    display: flex;
    flex-direction: column;
    align-items: center;

    .title {
      margin-top: 124px;
      color: #000000e6;
      text-align: center;
      font-size: 24px;
      font-style: normal;
      font-weight: 500;
      line-height: 28px;
      letter-spacing: 0.24px;
    }

    .evaluation-type {
      display: flex;
      margin: 40px 0;

      .evaluation-type-item {
        display: flex;
        padding: 8px 24px;
        justify-content: center;
        align-items: center;
        gap: 4px;
        flex: 1 0 0;
        border-radius: 3px 0 0 3px;
        border: 1px solid #DCDCDCFF;
        background: #FFF;
        cursor: pointer;

        text-align: center;
        font-size: 16px;
        font-style: normal;
        font-weight: 400;
        line-height: 24px;
      }

      .isSelected {
        color: #00A9CEFF;
        border-color: #00A9CEFF;
      }
    }

    .select-question-bank {
      display: flex;
      align-items: baseline;
      margin-right: 72px;
      margin-bottom: 30px;
    }

    .select-model {
      display: flex;
      align-items: baseline;
      margin-right: 72px;
      margin-bottom: 33px;
    }

    .submit-btn {
      width: 330px;
      height: 40px;
      padding: 8px 24px;
      border-radius: 3px;
      background: #00A9CE;
      border: 0;
      color: #ffffffe6;
      text-align: center;
      font-size: 16px;
      font-style: normal;
      font-weight: 400;
      line-height: 24px;
      cursor: pointer;
    }

    .label {
      margin-right: 16px;
      color: #00000080;
      text-align: right;
      font-size: 14px;
      font-style: normal;
      font-weight: 400;
      line-height: 22px;
    }

    .m-2 {
      font-size: 14px;
    }

    :deep(.el-input__wrapper) {
      padding: 5px 8px;
      width: 314px;
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
      color: #000000e6;
      text-overflow: ellipsis;
      white-space: nowrap;
      font-size: 14px;
      font-style: normal;
      font-weight: 400;
      line-height: 22px;
    }
  }
}
</style>
