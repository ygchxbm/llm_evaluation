<script setup lang="ts">
import {login} from "@/api";
import {onMounted, ref} from "vue";
import router from "@/router";

const isLoginBtn = ref(true);
const url = 'https://oasisdev.qq.com/oauth2/auth?client_id=CO7GBRGDJHBBDBMTCOT6CBGR25M&redirect_uri=https://lightpaw.com/Login&response_type=code&scope=openid+offline&state=Hy%2Bsb%2BWUGK0X50yBYf7FVzBhEZTMBDaPVXzqelHZUdY%3D'

const headerName = "Authorization";
onMounted(() => {
  let storedData = localStorage.getItem(headerName);
  // localStorage.removeItem(headerName);
  if (storedData) {
    storedData = JSON.parse(storedData);
    const currentTime = new Date().getTime();
    if (currentTime > storedData.expiration * 1000) {
      // 数据已过期，清除
      localStorage.removeItem(headerName);
      storedData = null;
      verify()
    } else {
      routeToLogin()
    }
  } else {
    verify()
  }
})

function verify() {
  const newUrl = document.URL;
  if (newUrl.includes('code=') && newUrl.includes('scope')) {
    const code: string = newUrl.split('code=')[1].split('&scope')[0];
    login(code).then(res => {
      if (res.code === 0) {
        const headerValue = `Bearer ${res.data.access_token}`;
        const expiration: number = res.data.expires_in;
        localStorage.setItem(headerName, JSON.stringify({value: headerValue, expiration: expiration}));
        isLoginBtn.value = false;
        routeToLogin()
      }
    }).catch(e => {
      console.info(e)
    })
  }
}

function routeToLogin() {
  router.push("/home")
}
</script>

<template>
  <div class="test">
    <a :href="url">{{ isLoginBtn ? '请验证' : '验证成功' }}</a>
  </div>

</template>

<style scoped lang="scss">
.test {
  width: 100%;
  height: 100vh;
  overflow: hidden;

  display: flex;
  justify-content: center;
  align-items: center;

  a {
    width: 120px;
    height: 50px;
    background: #48aacb;
    text-align: center;
    line-height: 50px;
    text-decoration: none;
    //color: #E7E7E7;
    color: #FFFFFF;
    font-size: 18px;
    border-radius: 3px;
    border: 0;
    margin: 20px;
  }

  .el-button {
    width: 120px;
    height: 50px;
    background: #48aacb;
    text-align: center;
    line-height: 50px;
    text-decoration: none;
    //color: #E7E7E7;
    color: #FFFFFF;
    font-size: 18px;
    border-radius: 3px;
    border: 0;
    margin: 20px;
  }


  .header {
    width: calc(100% - 60px);
    height: 300px;
    background: lightpink;
    margin: 30px;
  }

  .detail {
    width: 100%;
    height: 100%;
    padding: 30px;
    background: lightcoral;;
  }
}
</style>
