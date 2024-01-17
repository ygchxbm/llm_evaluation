<script lang="ts" setup>

import {ref, computed, onMounted, reactive} from "vue";
import router from "@/router/index.js";
import {ElTable} from "element-plus";
import {questionSetList, modelList, modelItem} from "@/api"

const modelSizeData = [
  "小于1B", "1B～3B", "3B-7B", "7B-13B", "13B-40B", "40B以上"
]

const modelSizeDataMap = {
  "小于1B": [0, 1],
  "1B～3B": [1, 3],
  "3B-7B": [3, 7],
  "7B-13B": [7, 13],
  "13B-40B": [13, 40],
  "40B以上": [40, Infinity],
}

const modelTypeData = [
  "预训练", "微调",
]

const checkEvaluationMode = ref<string[]>([]);
const checkModelSize = ref(["小于1B"]);
const checkModelTypeData = ref(['Option1']);

// let questionBankNames: {} = reactive({});
// let questionScores: {} = reactive({});
let modeNameList: string[] = reactive([]);
const modeDatalist = ref<modelItem[]>([]);


const tableData = computed(() => {
  if (modeDatalist.value.length > 0) {
    const questionScores = {}
    // console.info("checkModelSize:", checkModelSize.value)
    const ranges = checkModelSize.value.map(sizeText => {
      return Reflect.get(modelSizeDataMap,sizeText)
    })
    // console.info("ranges:", ranges)
    // const res=isRange(ranges,1024)
    // console.info("res:", res)
    modeNameList = [];
    modeDatalist.value.filter((item => {
      return isRange(ranges, item.scale)
    })).forEach(item => {
      modeNameList.push(item.model_name);
      const tmpObj = JSON.parse(item.score_detail_question_set);
      if (tmpObj) {
        const modeName = Reflect.get(item, 'model_name');
        Reflect.set(questionScores, modeName, {});
        const questionBankIds = Reflect.ownKeys(questionBankNames.value);
        questionBankIds.forEach(questionBankId => {
          let questionBankScore = Reflect.get(tmpObj, questionBankId);
          const questionBankName = Reflect.get(questionBankNames.value, questionBankId);
          if (typeof questionBankScore === "number") {
            questionBankScore = parseFloat(questionBankScore.toFixed(4))
          }
          Reflect.set(Reflect.get(questionScores, modeName), questionBankName, questionBankScore);
          // questionScores[modeName].push(obj)
        })
      }
    })

    // console.info("result:", result)
    // return result
    const tableData: object[] = [];

    modeNameList.forEach(modeName => {
      const obj = {};
      tableHeads.value.forEach((questionBankName, index) => {
        let value;
        if (index === 0) {
          value = modeName
        } else if (Reflect.get(questionScores, modeName)) {
          value = Reflect.get(Reflect.get(questionScores, modeName), questionBankName)
        }
        Reflect.set(obj, questionBankName, value);
      })
      tableData.push(obj);
    })
    return tableData
  }


  function isRange(ranges: [][], num: number): boolean {
    let res = false;
    const rangesLength = ranges.length;
    for (let i = 0; i < rangesLength; i++) {
      const range: number[] = ranges[i];
      const min: number = range[0];
      const max: number = range[1];
      const tempNum: number = num / 1024;
      if (min < tempNum && tempNum <= max) {
        res = true;
        break
      }
    }
    return res
  }
})

onMounted(async () => {
  await questionSetList().then(res => {
    // console.info("names:", res)
    res.forEach(item => {
      const questionBankId = item.id;
      const questionBankName: string = item.name;
      Reflect.set(questionBankNames.value, questionBankId, questionBankName)
    })
    console.info("questionBankNames:", questionBankNames.value)
  }).catch(e => {
    console.info("e:", e)
  })

  await modelList().then(res => {
    console.info("scores:", res)
    modeDatalist.value = res;
  }).catch(e => {
    console.info(e)
  });
  Object.values(questionBankNames.value).slice(0, 5).forEach((questionBankName) => {
    checkEvaluationMode.value.push(questionBankName)
  });

})


function myChange() {
  // console.info("checkEvaluationMode.value:", checkEvaluationMode.value)
}

function startComparing() {
  router.push({name: "ModeComparison"})
}

interface User {
  date: string
  name: string
  address: string
}

interface QuestionBankNames{
  [propName:number]:string
}

const questionBankNames=ref<QuestionBankNames>({});
const multipleTableRef = ref<InstanceType<typeof ElTable>>()
const multipleSelection = ref<User[]>([])


const tableHeads = computed(() => {
  return ['Model'].concat(checkEvaluationMode.value)
})
const handleSelectionChange = (val: User[]) => {
  multipleSelection.value = val
}
</script>

<template>
  <div class="home">
    <div class="content">
      <div class="except-interactive-specification">
        <div class="evaluation-model parameter">
          <div class="label">评测任务：</div>
          <el-checkbox-group class="checkboxes" v-model="checkEvaluationMode" @change="myChange" size="large">
            <el-checkbox v-for="item in questionBankNames" :label="item" border/>
          </el-checkbox-group>
        </div>
        <div class="model-size parameter">
          <div class="label">模型大小：</div>
          <el-checkbox-group class="checkboxes" v-model="checkModelSize" @change="myChange" size="large">
            <el-checkbox v-for="item in modelSizeData" :label="item" border/>
          </el-checkbox-group>
        </div>
        <div class="model-type parameter">
          <div class="label">模型类别：</div>
          <el-checkbox-group class="checkboxes" v-model="checkModelTypeData" @change="myChange" size="large">
            <el-checkbox v-for="item in modelTypeData" :label="item" border/>
          </el-checkbox-group>
          <button class="compare-btn" @click="startComparing">对比</button>
        </div>
        <div class="mode-table">
          <el-table
              width="500ppx"
              height="414"
              ref="multipleTableRef"
              :data="tableData"
              @selection-change="handleSelectionChange"
              table-layout="auto"
              border
              fit
              scrollbar-always-on
          >
            <el-table-column type="selection" width="40"/>
            <el-table-column v-for="item in tableHeads" :prop="item" :label="item"/>
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

      .parameter {
        margin: 0 10px;
        display: flex;
        align-items: baseline;


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

      .evaluation-model {
      //padding-top: 30px; margin-top: 10px;
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
          background: #00A9CEFF;
          border: 0;
          color: #ffffffe6;
          text-align: center;
          font-size: 16px;
          font-style: normal;
          font-weight: 400;
          line-height: 24px;
          position: absolute;
          right: -10px;
          cursor: pointer;
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
</style>
