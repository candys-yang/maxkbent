<template>
  <el-container v-loading="loading">
    <el-aside style="width:auto">
      <el-menu 
        :default-active="currentActiveIndex"
        :collapse="true"
        router
        style="height: calc(100vh);">
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <template #title> 主页 </template>
        </el-menu-item>
        <el-menu-item index="/knowl">
          <el-icon><InfoFilled /></el-icon>
          <template #title> 知识 </template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main style="margin: 0px; padding: 0px; width:auto">
      <router-view v-slot="{ Component }">
        <transition name="fade"><component :is="Component" /></transition>
      </router-view>
    </el-main>
  </el-container>
</template>
    
<script lang="ts" setup>
  import {
    InfoFilled,
    Menu as IconMenu,
    HomeFilled,
    Tools,
  } from '@element-plus/icons-vue'
  import 'element-plus/theme-chalk/display.css'
  import { ElMessage } from 'element-plus'
  import { computed, ref } from 'vue';
  import { useRoute } from 'vue-router'
  import { LocalStorage } from '@/composables/store';
  
  const route = useRoute()
  const localstore = LocalStorage()

  const currentActiveIndex = computed(() => {
    return '/' + route.path.split('/')[1];
  });

  let loading = ref(false)


  console.info('Index.vue Mount.')

</script>
  
<style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
  .fade-enter-active {
    transition: opacity 0.2s; /* 立即跳到最终状态 */
  }

  .fade-enter-from {
    opacity: 0; /* 初始状态为完全透明 */
  }

  .fade-leave-active {
    transition: opacity 0s; /* 离开时逐渐过渡到完全透明 */
  }

  .fade-leave-to {
    opacity: 0; /* 最终状态为完全透明 */
  }


  /** 全局组件配置 */
  .el-button--small { padding: 2px 10px; font-size: 12px }
  .el-card__body { padding: 13px; }

</style>
  