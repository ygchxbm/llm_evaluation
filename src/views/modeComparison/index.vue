<script setup>
import {ArrowRight} from '@element-plus/icons-vue'
import {Search} from '@element-plus/icons-vue'
import {ref} from "vue";

const input3 = ref("");
const activeName = ref('first')
const handleClick = (tab, event) => {
}

const checkModelSize = ref(['Option1']);

const tabsData = ["Natural Questions_QA", "WebQuestions_QA", "TriviaQA_QA", "MMLU_subject", "AGIEval-EN_subject", "ARC-e_subject", "ARC-e_subject", "LAMBADA_Reason", "HellaSwag_Reason", "WinoGrande_Reason"]

const answerPresentationData = [
  {mode: "ERNIE-Bot", result: true},
  {mode: "xfSpark2", result: true},
  {mode: "qwen", result: true}
]

const detailData = [
  {
    title: "i don't agre. white people commit crimes just liek black, samoan, asian,question: is the passage above toxic?",
    items: [
      {
        mode: "ERNIE-Bot",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      },
      {
        mode: "xfSpark2",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: false
      },
      {
        mode: "qwen",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      }
    ]
  },
  {
    title: "i don't agre. white people commit crimes just liek black, samoan, asian,question: is the passage above toxic?",
    items: [
      {
        mode: "ERNIE-Bot",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      },
      {
        mode: "xfSpark2",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: false
      },
      {
        mode: "qwen",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      }
    ]
  },
  {
    title: "i don't agre. white people commit crimes just liek black, samoan, asian,question: is the passage above toxic?",
    items: [
      {
        mode: "ERNIE-Bot",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      },
      {
        mode: "xfSpark2",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: false
      },
      {
        mode: "qwen",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      }
    ]
  },
  {
    title: "i don't agre. white people commit crimes just liek black, samoan, asian,question: is the passage above toxic?",
    items: [
      {
        mode: "ERNIE-Bot",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      },
      {
        mode: "xfSpark2",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: false
      },
      {
        mode: "qwen",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      }
    ]
  },
  {
    title: "i don't agre. white people commit crimes just liek black, samoan, asian,question: is the passage above toxic?",
    items: [
      {
        mode: "ERNIE-Bot",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      },
      {
        mode: "xfSpark2",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: false
      },
      {
        mode: "qwen",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      }
    ]
  },
  {
    title: "i don't agre. white people commit crimes just liek black, samoan, asian,question: is the passage above toxic?",
    items: [
      {
        mode: "ERNIE-Bot",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      },
      {
        mode: "xfSpark2",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: false
      },
      {
        mode: "qwen",
        text: "i don't agre. white people commit crimes ,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?i don't agre. white people commit crimes just liek black,samoan,asian,question: is the passage above toxic?",
        result: true
      }
    ]
  },
]

function mychange() {

}
</script>

<template>
  <div class="model-details">
    <div class="breadcrumb">
      <el-breadcrumb :separator-icon="ArrowRight">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>模型对比</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="content">
      <div class="search">
        <div class="label">搜索</div>
        <div>
          <el-input
              v-model="input3"
              class="w-50 m-2"
              size="small"
              placeholder="请输入关键词"
              :suffix-icon="Search"
          />
        </div>
      </div>
      <div class="tabs">
        <el-tabs v-model="activeName" class="demo-tabs" @tab-click="handleClick">
          <el-tab-pane v-for="item in tabsData" :label="item" :name="item"></el-tab-pane>
        </el-tabs>
      </div>
      <div class="answer-presentation">
        <div class="label">答案展示：</div>
        <div class="checkboxes">
          <div class="checkbox-group" v-for="item in answerPresentationData">
            <div class="checkbox-label">{{ item.mode }} :</div>
            <el-checkbox label="对"/>
            <el-checkbox label="错"/>
          </div>
        </div>
      </div>
      <div class="showDetails">
        <div class="detail" v-for="(tempDetail,index) in detailData">
          <div class="title">{{ index < 9 ? "0" + (index + 1) + '  ' : index + 1 + '  ' }}{{ tempDetail.title }}</div>
          <div class="texts">
            <div class="item" :class="{'item_false':!item.result}" v-for="item in tempDetail.items">
              <div class="item-title">
                <div class="mode">{{ item.mode }}</div>
                <div class="logo" :class="{'logo_false':!item.result}">{{ item.result ? "√" : "x" }}</div>
              </div>
              <div class="text">{{ item.text }}</div>
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
      }

      :deep(.el-tabs__item.is-top.is-active) {
        color: #00a9ce;
        font-size: 14px;
        font-style: normal;
        font-weight: 500;
        line-height: 40px;
      }

      :deep(.el-tabs__nav-wrap::after){
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
        //width: 220px; height: 44px; flex-shrink: 0; border-radius: 6px; border: 1px solid #E7E7E7; background: linear-gradient(180deg, #FFF 0%, #F8F8F8 100%); box-shadow: 0 2px 2px 0 #00000005; margin-right: 20px;

          .checkbox-label {
            margin: 0 16px;
            color: #000000e6;
            text-align: right;
            font-size: 14px;
            font-style: normal;
            font-weight: 400;
            line-height: 22px;
          }

          .el-checkbox {
            width: 38px;
            margin-right: 15px;
            color: #000000e6;
            font-size: 14px;
            font-style: normal;
            font-weight: 400;
            line-height: 22px;
            box-sizing: content-box;
          }

          :deep(.el-checkbox__label){
            font-size: 14px;
            font-style: normal;
            font-weight: 400;
            line-height: 22px;
          }

          :deep(.el-checkbox__input .el-checkbox__inner){
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
            height: 270px;
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
              }

              .logo_false {
                background: #E34D59FF;
              }
            }

            .text {
            //width: 480px; height: 191px; flex-shrink: 0; color: #000000b3;
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
