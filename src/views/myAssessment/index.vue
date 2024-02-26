<script setup lang="ts">
import {onMounted, ref} from "vue";
import {ElTable} from "element-plus";
import type {TableColumnCtx} from 'element-plus'
import {modelList, questionSetItem, questionSetList, examList, ExamListItem, questionSetListForAuto, questionSetItemForAuto, userList} from "@/api";
import {computedAsync} from "@vueuse/core";

//所有发起人
const initiatorOptionsMap = ref<Map<string, string>>(new Map());

//已选择的发起人
const selectedInitiator = ref<string>("");
//已选择的时间
const selectedTime = ref<string>();
//所有的modeName
const modeOptions = ref<string[]>([]);
//已选择的模型name
const selectedMode = ref<string>("");

const questionBankList = ref<questionSetItem[]>([]);
const questionBankNames = ref<{
  [prop: number]: string
}>({});//{questionBankId:questionBankName}
let modeNameList = ref<{
  [prop: number]: string
}>({});//{modeId:modeName}
let questionScores = ref<object>({});//{modeId:{questionBankName:score}}
// const examDataList = ref<ExamListItem[]>([]);

//月份英文缩写与月份数组的映射表
const monthMap: {
  [prop: string]: string
} = {
  Jan: '01',
  Feb: '02',
  Mar: '03',
  Apr: '04',
  May: '05',
  Jun: '06',
  Jul: '07',
  Aug: '08',
  Sept: '09',
  Oct: '10',
  Nov: '11',
  Dec: '12'
}

//表头
const tableHeaders = ['发起人', '评测时间', '模型名称', '题库', '分数'];

interface Row {
  "发起人": string;
  "评测时间": string;
  "模型名称": string;
  "题库": string | undefined;
  "分数": number;
  id: number
}

const tableData = computedAsync(async () => {
  if (initiatorOptionsMap.value.size === 0) return []
  let examDataList: ExamListItem[] = [];
  let option = {
    page_size: 9999,
  }
  if (selectedInitiator.value === '') {
    Reflect.set(option, 'create_user_id', parseInt(selectedInitiator.value))
  }

  //用作收集依赖
  if (selectedMode.value || selectedTime.value) {
  }


  await examList(option).then(res => {
    if (res) {
      examDataList = res.items
    }
  }).catch(e => {
    console.info(e)
  });


  const tempResult: Row[] = []
  if (examDataList && examDataList.length > 0) {
    examDataList.forEach(item => {
      const initiatorName = item.create_user_id + '_' + item.create_user;
      const modeName = modeNameList.value[item.llm_model_id];
      const obj: Row = {
        '发起人': initiatorName,
        '评测时间': parseTime(item.updated_at),
        '模型名称': modeName,
        '题库': questionBankNames.value[item.question_set_id],
        '分数': item.submit_score,
        id: item.question_set_id
      };
      if (!modeOptions.value.includes(modeName)) {
        modeOptions.value.push(modeName)
      }
      if ((initiatorName === initiatorOptionsMap.value.get(selectedInitiator.value) || !selectedInitiator.value)
          && (modeName === selectedMode.value || !selectedMode.value)
          && (parseTime(item.updated_at) === selectedTime.value || !selectedTime.value)) {
        tempResult.unshift(obj)
      }
    })
  }

  //合并单元格
  let i = 0;
  const length = tempResult.length;
  if (length > 0) {
    let activeIndex = 0;
    const startIndexObj: {
      [props: number]: number
    } = {}
    mergeData.value = {
      startIndexObj: startIndexObj,
      mergeIndex: [],
    };
    let mergeLength = 1;
    while (i < length - 1) {
      const questionId = tempResult[i].id;
      const queGroupId = Reflect.get(questionGroupMap.value, questionId);
      const questionId2 = tempResult[i + 1].id;
      const queGroupId2 = Reflect.get(questionGroupMap.value, questionId2);
      if (queGroupId && queGroupId2 && queGroupId === queGroupId2) {
        mergeLength++
        if (mergeLength === 2) {
          activeIndex = i;
        }
        Reflect.set(startIndexObj, activeIndex, mergeLength)
      } else {
        mergeLength = 1;
      }
      i++
    }

    for (const index in startIndexObj) {
      const length = startIndexObj[index];
      for (let i = 0; i < length; i++) {
        if (i !== 0) {
          mergeData.value.mergeIndex.push(parseInt(index) + i)
        }
      }
    }
  }


  // console.info("mergeData:", mergeData.value)
  return tempResult
})

//解析时间格式
function parseTime(timeStr: string): string {
  const items = timeStr.split(' ');
  const year = items[3];
  const month = monthMap[items[2]];
  const day = items[1];
  return year + '-' + month + '-' + day;
}

const questionBankListForAuto = ref<questionSetItemForAuto[]>([]);

onMounted(async () => {
  await questionSetList().then(res => {
    questionBankList.value = res;
    res.forEach(item => {
      const questionBankId = item.id;
      const questionBankName: string = item.name;
      Reflect.set(questionBankNames.value, questionBankId, questionBankName)
    })
  }).catch(e => {
    console.info(e)
  })

  await modelList().then(res => {
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
  }).catch(e => {
    console.info(e)
  });

  await questionSetListForAuto().then(res => {
    if (res) {
      questionBankListForAuto.value = res;
    }
  })

  if (questionBankListForAuto.value && questionBankListForAuto.value.length > 0) {
    questionBankListForAuto.value.forEach(questionGroup => {
      const queGroupId = questionGroup.id;
      const questions = questionGroup.question_set_list;
      if (questions && questions.length > 0) {
        questions.forEach(question => {
          const questionId = question.id;
          Reflect.set(questionGroupMap.value, questionId, queGroupId);
        })
      }
    })

    // console.info("questionGroupMap:", questionGroupMap.value)
  }


  await userList().then(res => {
    if (res) {
      res.forEach(item => {
        const {id, name} = item
        const initiatorName = id + '_' + (name ? name : "");
        if (!initiatorOptionsMap.value.has(id.toString())) {
          initiatorOptionsMap.value.set(id.toString(), initiatorName)
        }
      })
    }
  })

  interface StoredData {
    expiration: number;
    value: string;
    userId: number
  }

  let storedDataJson: string | null = localStorage.getItem("Authorization");
  if (storedDataJson) {
    const storedData: StoredData = JSON.parse(storedDataJson);
    selectedInitiator.value = storedData.userId.toString();
  }
})

function filterData(data: Row[]) {
  return data.filter(item => {
    return (item['发起人'] === initiatorOptionsMap.value.get(selectedInitiator.value) || !selectedInitiator.value) && (item['模型名称'] === selectedMode.value || !selectedMode.value) && (item['评测时间'] === selectedTime.value || !selectedTime.value)
  })

}

const questionGroupMap = ref({})
const mergeData = ref<{
  startIndexObj: {
    [props: number]: number
  };
  mergeIndex: number[]
} | undefined>(undefined);

interface User {
  id: string
  name: string
  amount1: string
  amount2: string
  amount3: number
}

interface SpanMethodProps {
  row: User
  column: TableColumnCtx<User>
  rowIndex: number
  columnIndex: number
}

function spanMethod({rowIndex, columnIndex,}: SpanMethodProps) {
  if (mergeData.value) {
    if (mergeData.value.mergeIndex.includes(rowIndex) && (columnIndex === 0 || columnIndex === 1 || columnIndex === 2)) {
      return {
        rowspan: 0,
        colspan: 0,
      }
    }

    const length = mergeData.value.startIndexObj[rowIndex];
    if (length && (columnIndex === 0 || columnIndex === 1 || columnIndex === 2)) {
      return {
        rowspan: length,
        colspan: 1,
      }
    }
  }
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
                v-for="[id,initiatorName] in initiatorOptionsMap"
                :key="id"
                :label="initiatorName"
                :value="id"
            />
          </el-select>
        </div>
        <div class="evaluation-time">
          <span class="label">评测时间</span>
          <div class="select-time">
            <el-date-picker
                v-model="selectedTime"
                type="date"
                placeholder="请选择"
                value-format="YYYY-MM-DD"
                size="default"
                :teleported=false
            />
          </div>
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
      <!--      <div>{{tableData}}</div>-->
      <div class="mode-table">
        <el-table
            ref="multipleTableRef"
            :data="tableData"
            :span-method="spanMethod"
            style="width: 100%"
            max-height="1100"
            border
        >
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

      .evaluation-time {
        display: flex;
        align-items: baseline;

        :deep(.el-input__wrapper) {
          box-shadow: 0 0 0 1px #00A9CE inset;
        }

        :deep(.el-date-table td.today .el-date-table-cell__text) {
          color: #64ceff;
        }

        :deep(.el-date-table td.current .el-date-table-cell__text) {
          background: #64ceff;
        }
      }

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
