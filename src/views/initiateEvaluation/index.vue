<script setup lang="ts">
import {modelList, questionSetItem, questionSetItemForAuto, questionSetList, modelItem, createExam, examDetail, examItem, generateAnswer, questionSetListForAuto} from "@/api";
import {computed, onMounted, ref} from "vue";
import router from "@/router";
import {ElLoading, ElMessage} from 'element-plus'

const questionBankList = ref<questionSetItem[]>([]);
const questionBankListForAuto = ref<questionSetItemForAuto[]>([]);
const selectedQuestionBankId = ref<number>();
const modeDataList = ref<modelItem[]>([]);
const selectedModeId = ref<number>();
const selectedEvaluationType = ref("auto");

const selectedQuestionBankIds = ref<number[]>([]);

function changeQuestionBankIds(id: number) {
  selectedQuestionBankIds.value = [];
  selectedQuestionBankIds.value.push(id);
}

const selectedModeIds = ref<number[]>([]);

function changeModeIds(id: number) {
  selectedModeIds.value = [];
  selectedModeIds.value.push(id);
}

onMounted(async () => {
  await questionSetList().then(res => {
    questionBankList.value = res;
    res.forEach(item => {
      const {id, name} = item;
      allQueBankIds.value.push(id);
      Reflect.set(allQueBankIdMap.value, id, name);
    })
    // console.info("questionSetList:", res)
  }).catch(e => {
    console.info(e)
  })

  // console.info("allQueBankIdMap:", allQueBankIdMap)

  await modelList().then(res => {
    modeDataList.value = res;
    res.forEach(item => {
      const {id, model_name} = item;
      allModeIds.value.push(id);
      Reflect.set(allModeIdMap.value, id, model_name);
    })
    // console.info("modelList:", res)
  }).catch(e => {
    console.info(e)
  });

  await questionSetListForAuto().then(res => {
    if (res) {
      questionBankListForAuto.value = res;
      res.forEach(item => {
        const queBankGroupId = item.id;
        const queBankGroupName = item.name;
        allQueBankIdsForAuto.value[queBankGroupId] = [];
        Reflect.set(allQueBankGroupIdMap.value, queBankGroupId, queBankGroupName);
        if (item.question_set_list && item.question_set_list.length > 0) {
          item.question_set_list.forEach(que => {
            const {id, name} = que;
            allQueBankIdsForAuto.value[queBankGroupId].push(id);
            Reflect.set(allQueBankIdMapForAuto, id, name);
          })
        }
        // allQueBankIds.value.push(id);
        // Reflect.set(allQueBankIdMap.value, id, name);
      })
      // console.info("allQueBankIdsForAuto:", allQueBankIdsForAuto)
      // console.info("allQueBankIdMapForAuto:", allQueBankIdMapForAuto)
    }
    // console.info("questionSetList:", res)
  }).catch(e => {
    console.info(e)
  })
})

function changeEvaluationType(val: string) {
  selectedQuestionBankId.value = undefined;
  selectedModeId.value = undefined;
  selectedEvaluationType.value = val;

  selectedQuestionBankIds.value = [];
  selectedModeIds.value = [];
}

async function submit() {
  if (selectedEvaluationType.value === 'auto') {
    if (selectedQuestionBankIds.value.length === 0) {
      alert('请选择题库')
    } else {
      await createExam(selectedQuestionBankIds.value, selectedModeIds.value, 2).then(res=>{
        // console.info("res:", res)
        if(res){
          ElMessage({
            message: "提交成功，请到'我的评测'查看",
            type: 'success',
          })
        }
      }).catch(e=>{
        console.error(e)
      })
    }
  } else if (selectedEvaluationType.value === 'artificial') {
    if (selectedQuestionBankIds.value.length === 0 && selectedModeIds.value.length > 0) {
      alert('请选择题库')
    } else if (selectedQuestionBankIds.value.length > 0 && selectedModeIds.value.length === 0) {
      alert('请选择模型')
    } else if (selectedQuestionBankIds.value.length === 0 && selectedModeIds.value.length === 0) {
      alert('请选择题库和模型')
    } else {
      // if (selectedQuestionBankIds.value.length===0 || selectedModeId.value === undefined) return

      //创建遮罩
      const loading = ElLoading.service({
        lock: true,
        text: 'Loading',
        background: 'rgba(0, 0, 0, 0.7)',
      })

      // setTimeout(() => {
      //   loading.close();
      // }, 60000)

      //创建评测任务，获取评测任务id
      let examIds: number[] = [];
      await createExam(selectedQuestionBankIds.value, selectedModeIds.value, 2).then(async res => {
        if (res) {
          examIds = res;
        }
      }).catch(e => {
        loading.close();
        console.info(e)
      })
      if (examIds.length !== 1) return

      //获取评测详情，不含ai答案
      let examItem: examItem | null = null;
      await examDetail(examIds[0]).then(res => {
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
        await generateAnswer(examIds[0], examItem.questions[i].id);
      }

      loading.close();
      console.info("examIds:", examIds[0])
      await router.push({
        name: "EvaluateDetail",
        query: {
          examId: examIds[0]
        }
      });
    }
  }
}

const mySelectedQueBankIds = ref<string[]>([]);
const allQueBankIds = ref<number[]>([]);
const allQueBankIdsForAuto = ref<{ [prop: number]: number[] }>({});
const allQueBankIdMap = ref<{
  [prop: number]: string
}>({});
const allQueBankGroupIdMap = ref<{
  [prop: number]: string
}>({});
const allQueBankIdMapForAuto = ref<{
  [prop: number]: string
}>({});
const allModeIds = ref<number[]>([]);

const allModeIdMap = ref<{
  [prop: number]: string
}>({});

interface QueBank{
  value:number;
  label:string;
  children:QueBankChild[]
}

interface QueBankChild{
  value:number;
  label:string;
}


const allQueBankIdsForAutoOptions = computed(() => {
  const result:QueBank[] = []
  if (allQueBankIdsForAuto.value && Object.keys(allQueBankIdsForAuto.value).length > 0) {
    Object.keys(allQueBankIdsForAuto.value).forEach(queBankGroupId => {
      const obj:QueBank = {
        value: parseInt(queBankGroupId) ,
        label: allQueBankGroupIdMap.value[parseInt(queBankGroupId)],
        children: []
      }
      const item = allQueBankIdsForAuto.value[parseInt(queBankGroupId)];
      item.forEach(queBankId => {
        const obj1:QueBankChild = {
          value: queBankId,
          label: allQueBankIdMap.value[queBankId],
        }
        obj.children.push(obj1)
      })
      result.push(obj)
    })
    return result
  }
})

function changeCascader(value: number[][]) {
  if (value.length > 0) {
    selectedQuestionBankIds.value = []
    value.forEach(item => {
      selectedQuestionBankIds.value.push(item[1])
    })
  }
}

const props = {multiple: true}
</script>

<template>
  <div class="initiate-evaluation">
    <div class="content">
      <div class="title">发起测评</div>
      <div class="evaluation-type">
        <div class="evaluation-type-item" @click="changeEvaluationType('auto')" :class="{'isSelected':selectedEvaluationType==='auto'}">自动评测</div>
        <div class="evaluation-type-item" @click="changeEvaluationType('artificial')" :class="{'isSelected':selectedEvaluationType==='artificial'}">人工评测</div>
      </div>
      <div v-if="selectedEvaluationType==='auto'">
        <!--        <div class="parameter">-->
        <!--          <div class="label">选择题库：</div>-->
        <!--          <el-checkbox-group class="checkboxes" v-model="mySelectedQueBankIds" size="large">-->
        <!--            <el-checkbox v-for="id in allQueBankIds" :label="id" border>{{ allQueBankIdMap[id] }}</el-checkbox>-->
        <!--          </el-checkbox-group>-->
        <!--        </div>-->
        <!--        <div class="parameter">-->
        <!--          <div class="label">选择模型：</div>-->
        <!--          <el-checkbox-group class="checkboxes" v-model="mySelectedModeIds" size="large">-->
        <!--            <el-checkbox v-for="id in allModeIds" :label="id" border>{{ allModeIdMap[id] }}</el-checkbox>-->
        <!--          </el-checkbox-group>-->
        <!--        </div>-->
        <div class="select-model">
          <span class="label">选择模型</span>
          <el-select v-model="selectedModeId" @change="changeModeIds" class="m-2" placeholder="请选择" size="small">
            <el-option
                v-for="item in modeDataList"
                :key="item.id"
                :label="item.model_name"
                :value="item.id"
            />
          </el-select>
        </div>
        <div class="select-question-bank">
          <div class="label">选择题库</div>
          <el-cascader
              :options="allQueBankIdsForAutoOptions"
              :props="props"
              v-model="mySelectedQueBankIds"
              @change="changeCascader"
              placeholder="请选择"
              collapse-tags
              collapse-tags-tooltip
              clearable
          />
        </div>
      </div>
      <div v-else>
        <div class="select-model">
          <span class="label">选择模型</span>
          <el-select v-model="selectedModeId" @change="changeModeIds" class="m-2" placeholder="请选择" size="small">
            <el-option
                v-for="item in modeDataList"
                :key="item.id"
                :label="item.model_name"
                :value="item.id"
            />
          </el-select>
        </div>
        <div class="select-question-bank">
          <span class="label">选择题库</span>
          <el-select v-model="selectedQuestionBankId" @change="changeQuestionBankIds" class="m-2" placeholder="请选择" size="small">
            <el-option
                v-for="item in questionBankList"
                :key="item.id"
                :label="item.name"
                :value="item.id"
            />
          </el-select>
        </div>
      </div>
      <el-button class="submit-btn" @click="submit()">发布
      </el-button>
    </div>
  </div>
</template>

<!--suppress CssNonIntegerLengthInPixels, CssUnusedSymbol -->
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

    .parameter {
      margin: 20px;
      display: flex;
      align-items: baseline;
      max-width: 800px;


      .label {
        min-width: 80px;
        font-size: 14px;
      }

      .checkboxes {
        display: flex;
        flex-wrap: wrap;
        margin-left: 15px;

        .el-checkbox {
          margin-right: 10px;
          margin-bottom: 10px;
          background: linear-gradient(180deg, #FFF 0%, #F8F8F8 100%);
          border-radius: 6px;
          border-color: #E7E7E7FF;
          color: #000000E6;
        }

        .el-checkbox.is-checked {
          border-color: #48aacb;
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
      box-shadow: 0 0 0 1px #00A9CE inset;
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
