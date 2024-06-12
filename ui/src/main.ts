import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import { ElLoading } from 'element-plus'
import 'uno.css'
import 'element-plus/dist/index.css'
import './assets/loading.css'
import { createRouter, RouteRecordRaw, createWebHashHistory } from 'vue-router';
// @ts-ignore
import axios from 'axios';
//
import App from './App.vue'
import {LocalStorage} from './composables/store';
import routes from './composables/route'

//
const app = createApp(App)
const router = createRouter({ history: createWebHashHistory(), routes });
// 
app.use(router)
app.use(ElementPlus,  { size: 'small' })
app.mount('#app') 


let loadingInstance:any = null;

router.beforeEach((to, from, next) => {
  // 显示加载提示
  loadingInstance = ElLoading.service({
    body: true,
    text: '正在渲染界面...',
    //spinner:  'public-loading',
    //customClass: 'public-loading-cent ',
  });
  next();
});

router.afterEach(() => {
  // 加载完成后移除加载提示
  if (loadingInstance) {
    loadingInstance.close();
  }
});


//
axios.interceptors.request.use((config:any) => {
  // 添加请求头
  const itsm3_oauth = LocalStorage().getItem('maxkbent_oauth');
  if(itsm3_oauth){
    config.headers.token = itsm3_oauth.token
    config.headers.session = itsm3_oauth.session
  }
  config.headers.reqid = Math.random().toString(36).substring(2, 14);

  return config;
},(error:any) =>{
  // 请求错误执行代码
  return Promise.reject(error)
})
axios.interceptors.response.use((response:any) => {
  // 响应请求的业务代码
  if(response.data.status == -401){
    console.info('axios 拦截 -401 状态，跳转路由： /login')
    router.push('/login')
  }
  return response
}, (error:any) => {
  return Promise.reject(error)
})
app.config.globalProperties.$axios = axios;













