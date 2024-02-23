<script setup lang="ts">
import {login} from "@/api";
import {onMounted, ref} from "vue";
import router from "@/router";


interface StoredData {
  expiration: number;
  value: string;
  userId: number;
}

const isLoginBtn = ref(true);
const env = import.meta.env;
const redirectUri: string = env.VITE_REDIRECT_URL
const url = `https://oasisdev.qq.com/oauth2/auth?client_id=${env.VITE_CLIENT_ID}&redirect_uri=${redirectUri}&response_type=code&scope=openid+offline&state=Hy%2Bsb%2BWUGK0X50yBYf7FVzBhEZTMBDaPVXzqelHZUdY%3D`

const headerName = "Authorization";
onMounted(() => {
  let storedDataJson: string | null = localStorage.getItem(headerName);
  // localStorage.removeItem(headerName);
  if (storedDataJson) {
    const storedData: StoredData = JSON.parse(storedDataJson);
    const currentTime = new Date().getTime();
    if (currentTime > storedData.expiration * 1000) {
      // 数据已过期，清除
      localStorage.removeItem(headerName);
      storedDataJson = null;
      verify()
    } else {
      window.location.href = redirectUri.split('/Login')[0];
    }
  } else {
    verify()
  }
})

function verify() {
  const newUrl = document.URL;
  if (newUrl.includes('code=') && newUrl.includes('scope')) {
    const code: string = newUrl.split('code=')[1].split('&scope')[0];
    login(code, redirectUri).then(res => {
      if (res) {
        debugger
        const {access_token, expires_in} = res;
        const headerValue = `Bearer ${access_token}`;
        const userId: number = res.userinfo.id;
        localStorage.setItem(headerName, JSON.stringify({value: headerValue, expiration: expires_in, userId}));
        isLoginBtn.value = false;
        window.location.href = redirectUri.split('/Login')[0];
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
