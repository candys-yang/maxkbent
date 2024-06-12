<template>
  <router-view></router-view>
</template>

<style>

body { padding: 0px; margin: 0;}

#app {
  color: var(--ep-text-color-primary);
}

.element-plus-logo {
  width: 50%;
}

/* md 显示 */
.github-theme p    { font-size: 13px; margin-top: 7px; margin-bottom: 7px;}
.github-theme p  strong  { font-size: 13px; font-weight: bold }
.github-theme p  code { font-size: 13px;}
.github-theme code { background-color: #ecf6ec; }
.github-theme pre code {  padding: 5px; }
.github-theme li { font-size: 13px; }
.github-theme span { font-size: 13px; }
.github-theme h1   { font-size:22px; }
.github-theme h2   { font-size:21px; }
.github-theme h3   { font-size:20px; }
.github-theme h4   { font-size:19px; }
.github-theme h5   { font-size:18px; }





</style>


<script setup>
  import { watch } from 'vue';
  import { onBeforeMount } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { ElMessage } from 'element-plus'
  import { LocalStorage } from '@/composables/store';
  import { getQueryVariable } from '@/composables/jsutil'
  

  const route = useRoute()
  const router = useRouter()
  const localstore = LocalStorage()



  const CheckToken = () => {
    try { 
      if(localstore.getItem('maxkbent_oauth').expire <= Date.now() / 1000){
        logging.info('token 过期')
        router.push({path: '/login', query:{...router.query}})
        ElMessage({message: '登录失效，请重新登录。', type: 'error'})
      }
    }
    catch(err){
      console.info('读取 maxkbent_oauth 失败，跳转登录界面。')
      router.push({path: '/login', query:{...router.query}})
    }
  }


  // 监控路由变化
  watch(() => route.fullPath, (newPath, oldPath) =>{
    //  用户认证信息监控，过期跳转到登录路由
    if(newPath != '/login'){ 
      CheckToken() 
    }
  })

  if(getQueryVariable('vwork_login')){
    ElMessage({message: '企业微信，单点登录'})
    console.info('企业微信登录')
    const cookies = document.cookie.split(';');
    let maxkbnet_oauth = null
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim(); // 去除空格
      if (cookie.startsWith('maxkb_ent_token' + '=')) {
        maxkbnet_oauth = cookie.substring('maxkb_ent_token'.length + 1); // 返回cookie值（去除名称部分）
      }
    }
    if(maxkbnet_oauth == null){ 
      ElMessage({message: '企业微信单点登录失败，无效的 token', type: 'error'})
      console.info('企业微信单点登录失败，无效的 token ')
      window.location.href = '#/';
    }else{
        console.info('设置 maxkbent_oauth 鉴权信息')
        localstore.setItemJson('maxkbent_oauth',{
        expire: Date.now() / 1000 + 30000, 
        token: maxkbnet_oauth, 
        session: getQueryVariable('session')
      })
      document.cookie = 'maxkbent_oauth=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      window.location.href = '#/';
    }
    
  }else{
    CheckToken()
  }

</script>
