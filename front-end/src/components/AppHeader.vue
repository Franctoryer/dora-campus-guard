<template>
  <a-layout-header class="header">
    <div class="logo">哆啦哨兵</div>
    <a-menu
      v-model:selectedKeys="selectedKeys"
      theme="dark"
      mode="horizontal"
      :style="{ lineHeight: '64px' }"
    >
      <a-menu-item key="home" @click="router.push('/')">
        <template #icon><home-outlined /></template>
        首页
      </a-menu-item>
      <a-menu-item key="ai-search" @click="router.push('/ai-search')">
        <template #icon><search-outlined /></template>
        AI 智搜
      </a-menu-item>
      <a-menu-item key="sentiment" @click="router.push('/sentiment')">
        <template #icon><heart-outlined /></template>
        情感与主题
      </a-menu-item>
      <a-menu-item key="warning" @click="router.push('/warning')">
        <template #icon><warning-outlined /></template>
        异常预警
      </a-menu-item>
    </a-menu>
    <div class="theme-switch">
      <a-switch v-model:checked="isDarkMode" @change="toggleTheme">
        <template #checkedChildren>
          <bulb-filled />
        </template>
        <template #unCheckedChildren>
          <bulb-outlined />
        </template>
      </a-switch>
    </div>
  </a-layout-header>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  HomeOutlined,
  SearchOutlined,
  HeartOutlined,
  WarningOutlined,
  BulbFilled,
  BulbOutlined,
} from '@ant-design/icons-vue'

const router = useRouter()
const route = useRoute()
const selectedKeys = ref([route.name as string])
const isDarkMode = ref(false)

watch(
  () => route.name,
  (newName) => {
    selectedKeys.value = [newName as string]
  },
)

const toggleTheme = (checked: boolean) => {
  // 这里可以添加主题切换的逻辑
  document.body.classList.toggle('dark-theme', checked)
}
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  padding: 0 24px;
  width: 100%;
}

.logo {
  color: white;
  font-size: 20px;
  font-weight: bold;
  margin-right: 48px;
}

.theme-switch {
  margin-left: auto;
}

:deep(.ant-menu) {
  flex: 1;
}

:deep(.ant-switch) {
  background-color: #1890ff;
}

:deep(.ant-switch-checked) {
  background-color: #52c41a;
}
</style>
