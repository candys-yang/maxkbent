<template>
    <div style="padding: 10px" v-loading="loading" >
      <el-row>
        <el-col :span="24" style="padding:5px;">
          <el-card shadow="never">
            <el-descriptions
              class="margin-top"
              title="用户概览"
              :column="3">
              <template #extra>
                <!-- <el-button type="primary">Operation</el-button> -->
              </template>
              <el-descriptions-item label="用户名">{{ v_name }}
              </el-descriptions-item>
              <el-descriptions-item label="员工编号"> {{ v_staff_id }} </el-descriptions-item>
              <el-descriptions-item label="职称"> {{ v_staff_jobs }} </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </template>
    
  <script lang="ts" setup>
    import { ref } from 'vue';
    import axios, { AxiosResponse } from 'axios';
    import { ElMessage } from 'element-plus'
  
    let loading = ref(true)
    //
    let v_name = ref()
    let v_staff_id = ref()
    let v_staff_jobs = ref()
  
    // 下载权限信息  
    axios.get('api/overview/userinfo')
    .then((res:AxiosResponse) => { 
      if (res.data.status != '200'){
        ElMessage({message: '获取概览信息失败' + res.data.message, type: 'error'})
      }else{
        v_staff_id.value = res.data.results.staff_id
        v_name.value = res.data.results.username
        v_staff_jobs.value = res.data.results.staff_jobs
      }
    })
    .catch(()=>{
      ElMessage({message: '获取概览信息失败，服务器错误。  ', type: 'error'})
    })
    .finally(()=>{ 
      loading.value = false
    })
  
  
  </script>
    
  <style scoped>
    /* .el-menu-vertical-demo:not(.el-menu--collapse) {} */
    .margin-top { margin-top: 5px;}
  </style>
    