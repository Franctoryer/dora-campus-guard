<script setup lang="ts">
// import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <div class="home">
    <div class="content">
      <a-row :gutter="16">
        <a-col :span="6">
          <a-card title="今日舆情总数" :bordered="false">
            <template #extra><a-tag color="blue">实时</a-tag></template>
            <h2>1,234</h2>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card title="负面舆情" :bordered="false">
            <template #extra><a-tag color="red">需关注</a-tag></template>
            <h2>56</h2>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card title="正面舆情" :bordered="false">
            <template #extra><a-tag color="green">良好</a-tag></template>
            <h2>1,178</h2>
          </a-card>
        </a-col>
        <a-col :span="6">
          <a-card title="预警信息" :bordered="false">
            <template #extra><a-tag color="orange">注意</a-tag></template>
            <h2>12</h2>
          </a-card>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<style scoped>
.home {
  padding: 20px;
}

.content {
  margin-top: 24px;
}

h1 {
  font-size: 24px;
  margin-bottom: 24px;
}

h2 {
  font-size: 28px;
  margin: 0;
  color: #1890ff;
}
</style>
