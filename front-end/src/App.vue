<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
</script>

<template>
  <a-layout class="layout">
    <app-header />
    <a-layout-content class="content">
      <router-view />
    </a-layout-content>
  </a-layout>
</template>

<style scoped>
.layout {
  min-height: 100vh;
}

.content {
  padding: 24px;
  min-height: calc(100vh - 64px);
  background: #fff;
}

:deep(.dark-theme) {
  background: #141414;
  color: rgba(255, 255, 255, 0.85);
}
</style>
