<script setup lang="ts">

import {Question, questionSetDetail} from "@/api";
import {onMounted, ref} from "vue";

const props = defineProps({
  id: Number,
})

console.info("props:", props.id)

const selectedQuestionBank = ref<Question | {} | null>({});

onMounted(() => {
  if (props.id === undefined) return
  questionSetDetail(props.id).then(res => {
    if (res === null) {
      return
    }
    selectedQuestionBank.value = res;
  }).catch(e => {
    console.info("e:", e)
  })
})

</script>

<template>
  <div class="main_detail_123">
    <div class="header_detail_123">
      <div class="question-bank-title_detail_123">{{ (selectedQuestionBank as Question).name }}</div>
    </div>
    <ul class="question-list_detail_123">
      <li class="question_detail_123" v-for="item in (selectedQuestionBank as Question).questions">
        <div class="question-title_detail_123">{{ item.question }}</div>
        <span class="question-style_detail_123">{{ item.dimension }}</span>
        <div class="question-answer_detail_123">{{ item.answer }}</div>
      </li>
    </ul>
  </div>
</template>

<style scoped lang="scss">
.main_detail_123 {
  height: 100%;
  opacity: 1;
  border: 0 solid #979797ff;
  background: #ffffffff;
  box-shadow: 0 10px 14px 0 #0000001a;
  overflow-y: auto;

  .header_detail_123 {
    display: flex;
    justify-content: space-between;
    margin: 16px 16px 0 30px;

    .question-bank-title_detail_123 {
      margin-top: 14px;
      color: #000000e6;
      font-size: 28px;
      font-weight: bold;
      text-align: center;
      line-height: 28px;
      letter-spacing: 0.24px;
    }
  }

  .question-list_detail_123 {
    --width: 30px;
    width: calc(100% - 2 * var(--width));
    margin: 30px;

    .question_detail_123 {
      min-height: 150px;
      margin-top: 30px;

      .question-title_detail_123 {
        min-height: 26px;
        margin-bottom: 8px;
        opacity: 1;
        color: #000000e6;
        font-size: 16px;
        font-weight: bold;
        text-align: left;
        line-height: 26px;
      }

      .question-style_detail_123 {
        height: 24px;
        border-radius: 3px;
        opacity: 1;
        border: 1px solid #c6e8efff;
        background: #e8f9fdff;
        padding: 2px 11px;

        color: #00a9ceff;
        font-size: 12px;
        font-weight: 400;
        text-align: center;
        line-height: 20px;
      }

      .question-answer_detail_123 {
        margin-top: 8px;
        min-height: 84px;
        opacity: 1;
        color: #000000b3;
        font-size: 16px;
        font-weight: 400;
        text-align: left;
        line-height: 28px;
      }
    }
  }
}
</style>
