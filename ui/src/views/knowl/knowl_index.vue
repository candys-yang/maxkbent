<template>
    <div style="padding: 5px">
      <el-card shadow="never" style="height: calc(100vh - 70px);">
        <div ref="Chatbox" style="height: calc(100vh - 70px); overflow-y: auto;">
          <div v-for="(item) in items" :key="item.index">
            <el-row>
              <el-col :span="1" v-if="item.types == '0'" style="padding:15px;">
                <el-icon size="22" color="#aba"><Platform /></el-icon>
              </el-col>
              <el-col :span="1" v-if="item.types == '1'" style="padding:15px;">
                <el-icon size="22" color="#baa"><Avatar /></el-icon>
              </el-col>
              <el-col :span="22" style="padding-top: 10px;">
                  <MdPreview previewTheme="github" :modelValue="item.mkdata" />
                  <!-- <div v-if="item.index !== 0 && item.types === '0'" 
                    style="text-align: right; padding-right: 5%">
                    <el-button plain :icon="CircleCheck" circle />
                    <el-button plain :icon="CircleClose" circle />
                    <el-button plain :icon="Document" circle />
                  </div> -->
              </el-col>
            </el-row>  
          </div>
        </div>  
      </el-card>
      <el-card shadow="never" style="padding:10px; margin-top:5px; height:30px">
        <el-row>
          <el-col :span="22">
            <el-input
              resize="none"
              :autosize="{maxRows: 1}"
              type="textarea"
              v-model="input_text"
              placeholder="向 AI助手 发送消息。"
              class="input-with-select"
              @keydown.enter.native="handleShiftEnter($event)"
            >
            </el-input>
          </el-col>
          <el-col :span="2">
            <el-button v-if="chating" disabled style="height:28px;margin-left:5px">......</el-button>
            <el-button v-else  style="height:28px;margin-left:5px" @click="handleShiftEnter">发送</el-button>
          </el-col>
        </el-row>
      </el-card>
    </div>
  </template>
  
  <script lang="ts" setup>
    import { ref, reactive  } from 'vue';
    import axios, { AxiosResponse } from 'axios';
    import { ElMessage } from 'element-plus'
    import { 
      Search , Platform, Avatar, CircleCheck, CircleClose, 
      Document } from '@element-plus/icons-vue'
    //
    import { MdEditor,MdPreview, MdCatalog } from 'md-editor-v3';
    import 'md-editor-v3/lib/style.css';
    // 数据类型
    interface ChatItem {
      index: number
      types: string 
      mkdata: string
    }
    // 组件变量
    const Chatbox:any = ref(null)
    let loading = ref(false)
    let loadingsum = ref(0)
    let input_text = ref('');
    let items:ChatItem[] = reactive([])
    let items_index = 0
    items.push({ 
      index: 0,     // 自增字段
      types: '0',   // 0 是ai ，1 是人类，
      mkdata: 'Hi Hi Hi~ \r\n' + 
      '我是智能对话机器人，你可以通过我了解集团IT相关的知识、数据、案例等。\r\n' 
    })
    let chating = ref(false)
    let chatid = ref('')
    // 组件函数
    const loadingser = (i:number) => {
      loadingsum.value += i
      if(loadingsum.value >= 1){
        loading.value = true
      }else{
        loading.value = false
      }
    }
    const handleShiftEnter = (event:any) =>{
      if(!event.shiftKey){
        if (chating.value) {
          ElMessage({message: '你当前有未完成的对话，请等待AI完成当前会话。', type: 'info'})
        }else{
          if(input_text.value == ''){}
          else{
            SentData()
          }
        }
        event.preventDefault();
      }else{
        input_text.value += '\r\n'
      }
    }
  
    // ajax 函数
    const SentData = () => {
      chating.value = true
      items_index += 1
      //items.push({index: items_index, types: '1', mkdata: input_text.value})
      setTimeout(() => {Chatbox._value.scrollTop = Chatbox.value.scrollHeight},100)
      //
      axios({
        method: 'post', 
        url: 'api/knowl/sessiondata', 
        data:{chatid: chatid.value ,chat: input_text.value}
      })
      .then((res) => {
        //console.info(res)
      })
      .finally(()=>{ 
        chating.value = false
        Chatbox._value.scrollTop = Chatbox.value.scrollHeight
      })
      GetData()
      input_text.value = ''
    }
  
  
    const GetData = () => {
      axios.get('api/knowl/sessiondata?&chatid=' + chatid.value)
      .then((res:AxiosResponse) => {
        if(res.data.status != '200'){ return}
        for (let i = 0; i < res.data.results.data.length; i++) {
          const element = res.data.results.data[i];
          SetChatUI(element)
        } 
      })
      .finally(() => {
        if(chating.value){
          GetData()
        }
        setTimeout(() => {Chatbox._value.scrollTop = Chatbox.value.scrollHeight},100)
      })
    }
  
  
    // 更新数据到UI
    const SetChatUI = (el:any) => {
      let loss = true
      for (let i = 0; i < items.length; i++) {
        const element = items[i];
        if(element.index == el.index){
          items[i].mkdata = el.data
          items[i].types = el.type
          loss = false
        }
      }
      if(loss){
        items.push({
          index: el.index, 
          types: el.type, 
          mkdata: el.data
        })
      }
    }
  
    // 打开组件时，获取会话id
    axios.get('api/knowl/openchat').then((res:AxiosResponse) => {
      if(res.data.status != '200'){ 
        ElMessage({message: '拉取页面参数失败，' + res.data.message, type: 'error'})
      }
      else{
        chatid.value = res.data.results.chatid 
      }
    })
  
  </script>
    
  <style scoped>
    /* .el-menu-vertical-demo:not(.el-menu--collapse) {} */
    ::v-deep .el-card__body {
      padding: 0px
    }
  
    ::v-deep .md-editor-preview-wrapper { padding: 5px; padding-left: 10px }
  </style>
  
  