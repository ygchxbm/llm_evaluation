<script lang="ts" setup>

import {ref, computed, onMounted} from "vue";
import router from "@/router/index.js";
import {ElTable} from "element-plus";
import {questionSetList, modelList, modelItem, questionSetItem, questionSetListForAuto, questionSetItemForAuto} from "@/api"
import {ElCollapseTransition} from 'element-plus'
// fade/zoom
// import 'element-plus/lib/theme-chalk/base.css'

interface MyData {
  allQueBanks: AllQueBanks;
  allModes: AllModes;
  allScores: AllScores;
}

interface AllQueBanks {
  [prop: string]: QueBank;
}

interface QueBank {
  name: string;
  score?: number;
}

interface AllModes {
  [prop: number]: Mode;
}

interface Mode {
  name: string;
}

interface AllScores {
  [prop: number]: ModeWithScore
}

interface ModeWithScore {
  name: string;
  scale: number;
  type: number;
  qusBanks: AllQueBanks;
}

const data = ref<MyData>()

const multipleTableRef = ref<InstanceType<typeof ElTable>>()
const multipleSelection = ref<Row[]>([])

// const checkEvaluationTask = ref<{ [prop: number]: string }[]>([]);

const isFlagTaskBtn = ref(false);
const checkEvaluationTaskOption = computed<{ [prop: number]: { name: string } }>(() => {
  const result = {};
  if (selectedBankForArtificial.value && selectedBankForArtificial.value.length > 0) {
    selectedBankForArtificial.value.forEach(item => {
      const id: number = parseInt(Object.keys(item)[0]);
      const name = item[id];
      Reflect.set(result, id, {name})
    })
  }
  return result
})

const taskText = computed(() => {
  if (isFlagTaskBtn.value) {
    return '收起任务'
  } else {
    return '展开任务'
  }
})

const allQueBankIds = ref<number[]>([]);
const allQueBankIdsForAuto = ref<{ [prop: number]: number[] }>({});
const questionBankListForAuto = ref<questionSetItemForAuto[]>([]);
const allQueBankIdMap = ref<{ [prop: number]: string }>({});
const allQueBankGroupIdMap = ref<{ [prop: number]: string }>({});
const allQueBankIdMapForAuto = ref<{ [prop: number]: string }>({});

const allQueBankObjForArtificial = ref<{ [prop: number]: { name: string } }>({});

interface QueBank2 {
  value: number;
  label: string;
  children: QueBankChild[]
}

interface QueBankChild {
  value: number;
  label: string;
}


const allQueBankIdsForAutoOptions = computed(() => {
  const result: QueBank2[] = []
  if (allQueBankIdsForAuto.value && Object.keys(allQueBankIdsForAuto.value).length > 0) {
    Object.keys(allQueBankIdsForAuto.value).forEach(queBankGroupId => {
      const obj: QueBank2 = {
        value: parseInt(queBankGroupId),
        label: allQueBankGroupIdMap.value[parseInt(queBankGroupId)],
        children: []
      }
      const item = allQueBankIdsForAuto.value[parseInt(queBankGroupId)];
      item.forEach(queBankId => {
        const obj1: QueBankChild = {
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


const selectedBankForArtificial = ref<{ [prop: number]: string }[]>([]);
const selectedBankForAuto = ref<number[][]>([]);
const checkEvaluationTask = computed(() => {
  const objs: any[] = []
  selectedBankForAuto.value.forEach(item => {
    const bankId = item[item.length - 1];
    const obj = {[bankId]: allQueBankIdMap.value[bankId]};
    objs.push(obj);
  })
  return objs.concat(selectedBankForArtificial.value)
})



const props = {multiple: true}

function changeTaskBtn() {
  isFlagTaskBtn.value = !isFlagTaskBtn.value;
}


const modelSizeData = {
  '0,1': "小于1B",
  '1,3': "1B～3B",
  '3,7': "3B-7B",
  '7,13': "7B-13B",
  '13,40': "13B-40B",
  '40,Infinity': "40B以上",
}
const checkModelSize = ref<string[]>(['0,1']);
const modelTypeData = {
  '1': "预训练",
  '2': "微调"
}
const checkModelType = ref<string[]>(['1']);
const defaultTableHead = {'0': 'Model'};

const tableHeads = computed(() => {
  let result = Object.assign({}, defaultTableHead);
  if (checkEvaluationTask.value.length > 0) {
    checkEvaluationTask.value.forEach(item => {
      result = Object.assign(result, item)
    })
  }
  return result
})

interface Row {
  [prop: string]: number | string;
}

const tableData = computed<Row[]>(() => {
  const result = []
  if (data.value) {
    const {allModes, allScores} = data.value;
    for (const modeId in allModes) {
      const modeWithScore = allScores[modeId];
      const mode = allModes[modeId];
      if (mode) {
        const row: Row | {} = {};
        for (const key in tableHeads.value) {
          if (key === '0') {
            Reflect.set(row, key, mode.name)
          } else {
            let score
            if (modeWithScore && isRange(checkModelSize.value, modeWithScore.scale) && checkModelType.value.includes(modeWithScore.type.toString())) {
              score = modeWithScore?.qusBanks[key]?.score;
              if (typeof score === 'number') {
                score = parseFloat(score.toFixed(4));
              }
            } else {
              score = undefined
            }
            Reflect.set(row, key, score)
          }
        }
        result.push(row)
      }
    }
  }
  return result
})

onMounted(async () => {
  let quesBank: questionSetItem[] | null = null, modeList: modelItem[] | null = null;
  await questionSetList().then(res => {
    quesBank = res;
  }).catch(e => {
    console.error("e:", e)
  })

  await questionSetList(1).then(res => {
    if (res) {
      res.forEach(item => {
        const {id, name} = item;
        Reflect.set(allQueBankObjForArtificial.value, id, {'name': name});
      })
    }
  }).catch(e => {
    console.error("e:", e)
  })

  await modelList().then(res => {
    modeList = res;
  }).catch(e => {
    console.error(e)
  });

  if (quesBank && modeList) {
    const allQueBanks: AllQueBanks = {};
    (quesBank as questionSetItem[])?.forEach(item => {
      const queBank: QueBank = {
        name: item.name,
      };
      Reflect.set(allQueBanks, item.id, queBank);
      if (selectedBankForArtificial.value.length < 5) {
        const obj: {
          [prop: number]: string
        } = {};
        obj[item.id] = queBank.name
        selectedBankForArtificial.value.push(obj)
      }
    })
    const allModes: AllModes = {};
    const allScores: AllScores = {};
    (modeList as modelItem[])?.forEach(item => {
      const mode = {
        name: item.model_name,
      }
      if (item.score_detail_question_set) {
        const queBankScore = JSON.parse(item.score_detail_question_set);
        const qusBanks: AllQueBanks = {};
        for (const queBankId in queBankScore) {
          const score = Reflect.get(queBankScore, queBankId);
          const queBankName = Reflect.get(allQueBanks, queBankId);
          const queBank = {
            name: queBankName,
            score
          }
          Reflect.set(qusBanks, queBankId, queBank)
        }
        const score = {
          name: item.model_name,
          scale: item.scale,
          type: item.type_id,
          qusBanks
        }
        Reflect.set(allScores, item.id, score)
      }
      Reflect.set(allModes, item.id, mode)
      Reflect.set(modeNameMap, mode.name, item.id)
    })

    data.value = {
      allScores,
      allModes,
      allQueBanks
    }
  }

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
      })
    }
  }).catch(e => {
    console.error(e)
  })

  await questionSetList().then(res => {
    if (res) {
      res.forEach(item => {
        const {id, name} = item;
        allQueBankIds.value.push(id);
        Reflect.set(allQueBankIdMap.value, id, name);
      })
    }
  }).catch(e => {
    console.error(e)
  })
})

interface ModeNameMap {
  [prop: string]: number
}

const modeNameMap: ModeNameMap = {}

interface EvaluatedAboutId {
  modeId: number;
  queBankIdList: number[];
}

let compareData: EvaluatedAboutId[] = [];

function startComparing() {
  if (!isDisabled.value) {
    router.push({
      name: "ModeComparison",
      query: {
        compareData: JSON.stringify(compareData)
      }
    })
  }
}

const isDisabled = ref<boolean>(true);
const compareBtn = ref<HTMLElement | null>(null)

function handleSelectionChange(val: Row[]) {
  //勾选两个及以上，显示对比按钮
  if (compareBtn.value) {
    if (val.length >= 2 && val.length <= 5) {
      const myStyle: CSSStyleDeclaration = compareBtn.value.style;
      myStyle.cursor = 'pointer';
      myStyle.opacity = '1';
      isDisabled.value = false;
    } else {
      const myStyle: CSSStyleDeclaration = compareBtn.value.style;
      myStyle.cursor = 'not-allowed';
      myStyle.opacity = '0.5';
      isDisabled.value = true;
    }
  }


  compareData = [];
  val.forEach(rowData => {
    let modeId: number = 0;
    const queBankIdList: number[] = []
    for (const modeNameKey in rowData) {
      const item: number | string = rowData[modeNameKey];
      if (modeNameKey === '0') {
        modeId = modeNameMap[item as string]
      } else if (item || item === 0) {
        queBankIdList.push(parseInt(modeNameKey));
      }
    }
    if (modeId || modeId === 0) {
      const obj: EvaluatedAboutId = {
        modeId,
        queBankIdList
      }
      compareData.push(obj);
    }
  })
  multipleSelection.value = val
}

function isRange(ranges: string[], num: number): boolean {
  let res = false;
  const rangesLength = ranges.length;
  for (let i = 0; i < rangesLength; i++) {
    const range: string[] = ranges[i].split(',');
    const min: number = parseInt(range[0]);
    const max: number = parseInt(range[1]);
    const tempNum: number = num / 1024;
    if (min < tempNum && tempNum <= max) {
      res = true;
      break
    }
  }
  return res
}


</script>

<template>
  <div class="home">
    <div class="content">
      <div class="except-interactive-specification">
        <!--        <div>{{checkEvaluationTaskAfterFilter}}</div>-->
        <div class="evaluation-model parameter">
          <div class="label">评测任务(手动)：</div>
          <el-checkbox-group class="checkboxes" v-model="selectedBankForArtificial" size="large">
            <el-checkbox v-for="(queBank,id) in checkEvaluationTaskOption" :label="{[id]:(queBank as QueBank).name}" border>{{ queBank.name }}</el-checkbox>
          </el-checkbox-group>
          <div class="task-btn" @click="changeTaskBtn">{{ taskText }}</div>
        </div>
        <el-collapse-transition>
          <div v-show="isFlagTaskBtn" style="height: 300px" class="collapse">
            <el-checkbox-group class="checkboxes" v-model="selectedBankForArtificial" size="large">
              <el-checkbox v-for="(queBank,id) in allQueBankObjForArtificial" :label="{[id]:(queBank as QueBank).name}" border>{{ queBank.name }}</el-checkbox>
            </el-checkbox-group>
          </div>
        </el-collapse-transition>
        <div class="evaluation-model parameter">
          <div class="label">评测任务(自动)：</div>
          <div class="select-question-bank">
            <el-cascader
                :options="allQueBankIdsForAutoOptions"
                :props="props"
                v-model="selectedBankForAuto"
                placeholder="请选择"
                collapse-tags
                collapse-tags-tooltip
                clearable
            />
          </div>
        </div>
        <div class="model-size parameter">
          <div class="label">模型大小：</div>
          <el-checkbox-group class="checkboxes" v-model="checkModelSize" size="large">
            <el-checkbox v-for="(value,key) in modelSizeData" :label="key" border>{{ value }}</el-checkbox>
          </el-checkbox-group>
        </div>
        <div class="model-type parameter">
          <div class="label">模型类别：</div>
          <el-checkbox-group class="checkboxes" v-model="checkModelType" size="large">
            <el-checkbox v-for="(value,key) in modelTypeData" :label="key" border>{{ value }}</el-checkbox>
          </el-checkbox-group>
          <button class="compare-btn" ref="compareBtn" @click="startComparing">对比</button>
        </div>
        <div class="mode-table">
          <el-table
              width="500ppx"
              height="414"
              ref="multipleTableRef"
              :data="tableData"
              @select="handleSelectionChange"
              table-layout="auto"
              border
              fit
              scrollbar-always-on
          >
            <el-table-column type="selection" width="40"/>
            <el-table-column v-for="(name,id) in tableHeads" :prop="id.toString()" :label="name"></el-table-column>
          </el-table>
        </div>
      </div>
      <div class="interactive-specification">
        <div class="title">交互说明：</div>
        <div class="texts">
          <div class="text">1、 【对比按钮】默认不展示</div>
          <div class="text">2、批量选择，仅允许选择2～5个，选择后，再展示【对比按钮】</div>
          <div class="text">3、点击对比按钮跳转到模型详情</div>
        </div>
      </div>
    </div>
  </div>
</template>

<!--suppress CssUnusedSymbol -->
<style scoped>
.home {
  height: 100%;
  overflow: hidden;

  .content {
    height: calc(100% - 40px);
    margin: 20px;
    padding: 20px;
    border-radius: 15px;
    background: #FFFFFF;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow-y: auto;

    .except-interactive-specification {
      display: flex;
      flex-direction: column;

      .collapse {
        overflow-y: scroll;
        background: #f8f8f8;
        padding: 20px;
        margin: 10px 120px 10px 145px;
        box-shadow: 1px 1px 10px 3px #0000001a inset;

        .checkboxes {
          display: flex;
          flex-wrap: wrap;

          .el-checkbox {
            margin: 5px 0 5px 10px;
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

      .parameter {
        margin: 0 10px;
        display: flex;
        align-items: baseline;


        .label {
          min-width: 110px;
          font-size: 14px;
        }

        .checkboxes {
          display: flex;
          flex-wrap: wrap;
          margin-left: 15px;
          border-radius: 10px;

          .el-checkbox {
            margin: 5px 0 5px 10px;
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

      .evaluation-model {
        display: flex;

        .checkboxes {
          padding-right: 80px;
        }

        .task-btn {
          position: absolute;
          right: 40px;
          margin-top: 10px;
          background: #00A9CE;
          color: #f8f8f8;
          padding: 5px 12px;
          border-radius: 3px;
          cursor: pointer;
          z-index: 100;
        }

        .select-question-bank {
          margin: 5px 0 5px 23px;

          :deep(.el-cascader .el-input__wrapper) {
            margin: 10px;
          }
        }
      }

      .model-size {
        margin-top: 4px;
        margin-bottom: 4px;
      }

      .model-type {
        position: relative;

        .compare-btn {
          width: 80px;
          height: 40px;
          border-radius: 3px;
          border: 0;
          text-align: center;
          font-size: 16px;
          font-style: normal;
          font-weight: 400;
          line-height: 24px;
          position: absolute;
          right: -10px;
          background: #00A9CEFF;
          color: #ffffffe6;
          opacity: 0.5;
          cursor: not-allowed;
        }
      }

      .mode-table {
      //max-height: 414px; //width: 100%; max-width: calc(100% - 2px); margin-top: 10px; //overflow-y: auto;

        :deep(.el-table__cell) {
          height: 46px; /* 设置表格每个单元格样式 */
          box-sizing: border-box;
        }

        :deep(.cell) {
          height: 22px; /* 设置表格每个单元格内的文字格样式 */
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

        :deep(.el-table__body-header tr) {
          box-shadow: 0 1px 5px #e3e3e3; /* 设置表格头阴影*/
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

        :deep(.el-table__row :nth-child(2)) {
          color: #00a9ce; /* 设置第二列字体颜色 */
        }
      }
    }

    .interactive-specification {
      width: 511px;
      height: 186px;
      flex-shrink: 0;
      border-radius: 12px;
      border: 2px dashed #FD5A5A;
      background: #FFF;
      box-sizing: border-box;
      margin-left: 20px;
      margin-bottom: 60px;

      .title {
        margin: 13px 0 13px 19px;
        color: #000000ff;
        font-size: 14px;
        font-style: normal;
        font-weight: 400;
        line-height: 22px;
      }

      .texts {
        margin-left: 41px;
        color: #000000ff;
        font-size: 14px;
        font-style: normal;
        font-weight: 500;
        line-height: 24px;
      }
    }
  }
}

:deep(.el-cascader .el-input__wrapper) {
  min-height: 40px;
  --el-input-border-color: #00a9ce;
  --el-input-focus-border-color: #00a9ce;
  border-radius: 6px;
}

:deep(.el-cascader) {
  --el-border-color-hover: #00a9ce;
}

::-webkit-scrollbar-track-piece {
  background-color: #dddee0;
}


</style>
