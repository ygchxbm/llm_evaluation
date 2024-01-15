<script setup lang="ts">
import {computed, onMounted, ref} from "vue";
import {ElTable} from "element-plus";
import {modelList, questionSetItem, questionSetList, examList} from "@/api";

const selectModelData = [
  {
    value: 'ERNIE-Bot',
    label: 'ERNIE-Bot',
  },
  {
    value: 'Option2',
    label: 'Option2',
  }
]


const random = Math.random;

//
const questionBankList = ref<questionSetItem[]>([]);
const questionBankNames = ref<object>({});//{questionBankId:questionBankName}
let modeNameList = ref<object>({});//{modeId:modeName}
let questionScores = ref<object>({});//{modeId:{questionBankName:score}}
const examDataList = ref<[]>([]);

const initiatorOptions = ref<string[]>([]);
const selectedInitiator = ref<string>("");

const modeOptions = ref<string[]>([]);
const selectedMode = ref<string>("");

const myTableData = computed(() => {
  const modeLength = examDataList.value.length;
  if (modeLength === 0) {
    return []
  } else {
    let i = 0;
    const result: any[] = [];
    examDataList.value.forEach((item, i) => {
      const obj = {};
      tableHeaders.value.forEach((headerText, j) => {
        if (j === 0) {
          // console.info("item.create_user:", item.create_user)
          obj[headerText] = item.create_user_id + '_' + item.create_user;
          if (!initiatorOptions.value.includes(obj[headerText])) {
            initiatorOptions.value.push(obj[headerText]);
          }
        } else if (j === 1) {
          obj[headerText] = item.updated_at;
        } else if (j === 2) {
          obj[headerText] = modeNameList.value[item.llm_model_id];
          if (!modeOptions.value.includes(obj[headerText])) {
            modeOptions.value.push(obj[headerText]);
          }
        } else if (j === 3) {
          obj[headerText] = questionBankNames.value[item.question_set_id];
        } else if (j === 4) {
          obj[headerText] = item.submit_score;
        }
      })
      result.push(obj)
    })
    return filterData(result).reverse()
  }
})

onMounted(async () => {
  await questionSetList().then(res => {
    // console.info("names:", res)
    questionBankList.value = res;
    res.forEach(item => {
      const questionBankId = item.id;
      const questionBankName: string = item.name;
      Reflect.set(questionBankNames.value, questionBankId, questionBankName)
    })
    // console.info("questionBankNames.value:", questionBankNames.value)
  }).catch(e => {
    console.info("e:", e)
  })

  await modelList().then(res => {
    // console.info("scores:", res)
    res.forEach(item => {
      const modeId = item.id;
      const modeName = item.model_name;
      Reflect.set(modeNameList.value, modeId, modeName)
      const tmpObj = JSON.parse(item.score_detail_question_set);
      if (tmpObj) {
        const questionBankId = Reflect.ownKeys(tmpObj)[0];
        const questionBankScore = Reflect.get(tmpObj, questionBankId);
        const questionBankName = Reflect.get(questionBankNames.value, questionBankId);
        const modeName = Reflect.get(item, 'model_name');
        const obj = {};
        Reflect.set(obj, questionBankName, questionBankScore)
        Reflect.set(questionScores.value, modeName, obj);
      }
    })
    // console.info("questionBankNames:", questionBankNames.value)
    console.info("modeNameList:", modeNameList.value)
    // console.info("questionScores:", questionScores.value)
  }).catch(e => {
    console.info(e)
  });

  await examList({page_size: 9999, create_user_id: 4}).then(res => {
    examDataList.value = res.data.items;
    console.info("res:", res)
  })
})

const tableHeaders = computed(() => {
  // return ['发起人', '评测时间', 'Model'].concat(Object.values(questionBankNames.value))
  return ['发起人', '评测时间', '模型', '题库', '分数']
})

function filterData(data: object[]) {
  // if (selectedInitiator.value) {
  return data.filter(item => {
    return (item['发起人'] === selectedInitiator.value || !selectedInitiator.value)&&(item['模型'] === selectedMode.value || !selectedMode.value)
  })

}

</script>

<template>
  <div class="my-assessment">
    <div class="content">
      <div class="select-inputs">
        <div class="initiator">
          <span class="label">发起人</span>
          <el-select v-model="selectedInitiator" class="m-2" placeholder="请选择" size="small" :clearable=true>
            <el-option
                v-for="item in initiatorOptions"
                :key="item"
                :label="item"
                :value="item"
            />
          </el-select>
        </div>
        <div class="evaluation-time">
          <span class="label">评测时间</span>
          <el-select v-model="selectedMode" class="m-2" placeholder="请选择" size="small">
            <el-option
                v-for="item in selectModelData"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
        </div>
        <div class="model-type">
          <span class="label">模型</span>
          <el-select v-model="selectedMode" class="m-2" placeholder="请选择" size="small" :clearable=true>
            <el-option
                v-for="item in modeOptions"
                :key="item"
                :label="item"
                :value="item"
            />
          </el-select>
        </div>
      </div>
      <div class="mode-table">
        <el-table
            ref="multipleTableRef"
            :data="myTableData"
            style="width: 100%"
            max-height="1100"
            border>
          <el-table-column v-for="item in tableHeaders" :prop="item" :label="item"/>
        </el-table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.my-assessment {
  height: 100%;
  overflow: hidden;

  .content {
    width: calc(100% - 40px);
    height: calc(100% - 40px);
    margin: 20px;
    padding: 20px;
    border-radius: 15px;
    background: #FFFFFF;
    overflow: hidden;

    .select-inputs {
      display: flex;
      align-items: baseline;
      margin-top: 10px;
      margin-left: 18px;
      margin-bottom: 24px;

      .label {
        color: #00000080;
        text-align: right;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: 22px;
        margin-right: 16px;
      }

      :deep(.el-input__wrapper) {
        padding: 5px 8px;
        width: 184px;
        height: 22px;
        margin-right: 35px;
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
    }

    .mode-table {
      width: calc(100% - 2px);

      :deep(.el-table__body-header tr) {
        box-shadow: 0 1px 5px #e3e3e3; /* 设置表格头阴影*/
      }

      :deep(.el-table__header-wrapper .el-table__header thead) {
        box-shadow: 0 0 10px 10px rgb(250, 248, 248);
      }

      :deep(.el-table__cell) {
        height: 46px; /* 设置表格每个单元格样式 */
        box-sizing: border-box;
      }

      :deep(.cell) {
        padding: 0 10px; /* 设置表格每个单元格内的文字格样式 */
        height: 22px;
        flex: 1 0 0;
        overflow: hidden;
        color: #000000e6;
        text-align: center;
        text-overflow: ellipsis;
        white-space: nowrap;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: 22px;
        border-color: #E7E7E7;
      }

      :deep(.is-leaf.el-table__cell) {
        background: #F8F8F8; /* 设置表格头的背景的颜色 */
      }

      :deep(.el-checkbox__input .el-checkbox__inner):hover {
        border-color: #48aacb; /* 设置单个多选框悬浮时候的颜色 */
      }

      :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
        background-color: #48aacb; /* 设置单个多选框选中时候的颜色 */
        border-color: #48aacb;
      }

      :deep(.el-checkbox__input.is-indeterminate .el-checkbox__inner) {
        background-color: #48aacb; /* 设置总多选框部分选中时候的颜色 */
        border-color: #48aacb;
      }

      :deep(.el-table__row):hover td {
        background: #f8f8f8; /* 设置每行悬浮时候的背景颜色 */
      }

      :deep(.el-table__row :nth-child(3)) {
        color: #00a9ce; /* 设置第三列字体颜色 */
      }

    }

  }
}
</style>
