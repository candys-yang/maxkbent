<template>
    <div style="height: 60vh; width: 100vw">
      <el-row style="margin-top: 100px">
      <el-col :span="8" :offset="8">
        <el-card shadow="never" v-loading="loading">
          <div style="padding-bottom:20px"> 用户登录 </div>
          <div style="font-size: 10px; padding-bottom: 5px;"> 账号密码：maxkbent </div>
          <el-form :model="form" label-width="60px">
            <el-form-item label="用户名">
              <el-input v-model="form.name" @keydown.enter="submitForm()" />
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="form.pwd" type="password" 
              @keydown.enter="submitForm()" ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitForm()" 
              @keydown.enter="submitForm()" > 登录 </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>
    </div>
  </template>
    
  <script lang="ts" setup>
    import { useRoute } from 'vue-router'
    import { ref, reactive } from 'vue'
    // @ts-ignore
    import axios, { AxiosResponse } from 'axios';
    import { ElMessage } from 'element-plus'
    import {cipher} from '@/composables/code'
    import { LocalStorage } from '@/composables/store';
    //
    const route = useRoute()
    //
    const Cipher = cipher()
    const localstore = LocalStorage()
  
    //
    const form = reactive({
      name: '',
      pwd: ''
    })
   
    let loading = ref(false)
     
    /** 登录数据 */
    interface UserReq{
      name: string, 
      pwd: string
    }
    //
    
    /** 执行登录动作 */
    const submitForm = () => {
      loading.value = true
      //
      let userreq: UserReq = {
        name: form.name, 
        pwd: Cipher.encrypt(form.pwd)
      }
      //
      axios.post('api/auth/login', userreq )
      .then((res:AxiosResponse) => { 
        if (res.data.status != '200'){
          ElMessage({message: '登录失败，' + res.data.meg, type: 'error'})
        }else{
          ElMessage({message: '登录成功'})
          localstore.setItemJson('maxkbnet_oauth',{
            expire: res.data.results.expire,
            token: res.data.results.token, 
            session: res.data.results.session
          })
          window.location.href = '#/';
        }
      })
      .catch((err)=>{
        ElMessage({message: '登录失败，服务器状态异常。', type: 'error'})
        console.error(err)
        loading.value = false
      })
      .finally(()=>{ 
        loading.value = false
      })
    }
  
  
  
  
    </script>
    