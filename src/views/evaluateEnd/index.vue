<script setup lang="ts">
import '@fortawesome/fontawesome-free/css/all.css';
import router from "@/router";
import {useRoute} from "vue-router";
import {computed} from "vue";

const route = useRoute();
const tempRating: string = (route.query.score as string);

const score = computed(() => {
  if (tempRating.includes('.')) {
    const length = tempRating.split('.')[1].length;
    return parseFloat(tempRating).toFixed(length);
  } else {
    return parseFloat(tempRating) + '.0'
  }
})

const rating=computed(()=>{
  return parseInt(score.value)/2;
})

const text = '测评到此结束，感谢您的参与！';

function backHome() {
  router.push('/')
}
</script>

<template>
  <div class="main">
    <button class="back-home" @click="backHome">返回首页</button>
    <div class="content">
      <div class="icon"></div>
      <div class="text">{{ text }}</div>
      <div class="score">
        <span class="score-label">评分：</span>
        <span class="score-text">{{ score }}</span>
        <el-rate v-model="rating" clearable allow-half size="large" :colors="['#00A9CE','#00A9CE','#00A9CE']" disabled/>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.main {
  width: 100%;
  //height: 100%;
  height: 100vh;
  background-image: url("@/assets/bgForAnswer.png");
  background-size: cover;
  display: flex;
  justify-content: center;
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

  //.back-home:hover{
  //  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  //}

  .content {
    width: calc(100% - 540px);
    height: calc(100% - 120px);
    background: #FFFFFF;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);

    .icon {
      width: 76px;
      height: 76px;
      background-image: url("@/assets/check-circle.png");
    }

    .text {
      margin: 80px 0;
      color: #000000;
      font-size: 18px;
      font-weight: 500;
      text-align: left;
      line-height: 40px;
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
        min-width: 77px;
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
  }
}

:deep(.el-rate__icon) {
  font-size: 30px;
}
</style>
