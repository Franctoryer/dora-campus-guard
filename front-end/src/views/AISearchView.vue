<template>
  <div class="ai-search">
    <div class="search-container">
      <a-input-search
        v-model:value="searchText"
        placeholder="输入关键词进行智能搜索"
        enter-button
        size="large"
        @search="onSearch"
      >
        <template #prefix>
          <robot-outlined />
        </template>
      </a-input-search>

      <div class="search-filters">
        <a-form layout="vertical">
          <a-row :gutter="16">
            <a-col :span="8">
              <a-form-item label="情感分类">
                <a-select
                  v-model:value="selectedEmotions"
                  mode="multiple"
                  placeholder="请选择情感类型"
                  style="width: 100%"
                  :options="emotionOptions"
                  :max-tag-count="3"
                ></a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item label="主题分类">
                <a-select
                  v-model:value="selectedTopics"
                  mode="multiple"
                  placeholder="请选择主题类型"
                  style="width: 100%"
                  :options="topicOptions"
                  :max-tag-count="3"
                ></a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item label="时间范围">
                <a-range-picker
                  v-model:value="dateRange"
                  style="width: 100%"
                  :show-time="{ format: 'HH:mm' }"
                  format="YYYY-MM-DD HH:mm"
                  :placeholder="['开始时间', '结束时间']"
                ></a-range-picker>
              </a-form-item>
            </a-col>
          </a-row>
        </a-form>
      </div>
    </div>

    <div class="ai-summary" v-if="searchResults.length">
      <a-card :bordered="false" class="summary-card">
        <template #title>
          <div class="summary-title">
            <robot-outlined />
            <span>AI 总结助手</span>
            <a-button type="link" @click="refreshSummary">
              <template #icon><reload-outlined /></template>
              重新生成
            </a-button>
          </div>
        </template>
        <div class="summary-content">
          <a-spin :spinning="summaryLoading">
            <div class="summary-section">
              <h3>📊 数据概览</h3>
              <p>{{ aiSummary.overview }}</p>
            </div>
            <div class="summary-section">
              <h3>🎯 主要发现</h3>
              <ul>
                <li v-for="(finding, index) in aiSummary.findings" :key="index">{{ finding }}</li>
              </ul>
            </div>
            <div class="summary-section">
              <h3>💡 建议关注</h3>
              <ul>
                <li v-for="(suggestion, index) in aiSummary.suggestions" :key="index">
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </a-spin>
        </div>
      </a-card>
    </div>

    <div class="search-results" v-if="searchResults.length">
      <a-list :data-source="searchResults" :pagination="pagination" item-layout="vertical">
        <template #renderItem="{ item }">
          <a-list-item key="item.title">
            <a-list-item-meta>
              <template #title>
                <a :href="item.url">{{ item.title }}</a>
              </template>
              <template #description>
                <a-tag
                  :color="
                    item.sentiment === 'positive'
                      ? 'green'
                      : item.sentiment === 'negative'
                        ? 'red'
                        : 'blue'
                  "
                >
                  {{
                    item.sentiment === 'positive'
                      ? '正面'
                      : item.sentiment === 'negative'
                        ? '负面'
                        : '中性'
                  }}
                </a-tag>
                <span class="time">{{ item.time }}</span>
              </template>
            </a-list-item-meta>
            {{ item.content }}
          </a-list-item>
        </template>
      </a-list>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { RobotOutlined, ReloadOutlined } from '@ant-design/icons-vue'
import type { Dayjs } from 'dayjs'

const searchText = ref('')
const selectedEmotions = ref<string[]>([])
const selectedTopics = ref<string[]>([])
const dateRange = ref<[Dayjs, Dayjs] | null>(null)
const summaryLoading = ref(false)

const emotionOptions = [
  {
    label: '消极',
    options: [
      { label: '悲伤', value: 'sad' },
      { label: '失望', value: 'disappointed' },
      { label: '讨厌', value: 'dislike' },
    ],
  },
  {
    label: '中性',
    options: [
      { label: '平和', value: 'calm' },
      { label: '疑惑', value: 'confused' },
    ],
  },
  {
    label: '积极',
    options: [
      { label: '开心', value: 'happy' },
      { label: '期待', value: 'expecting' },
    ],
  },
]

const topicOptions = [
  { label: '投稿', value: 'post' },
  { label: '求助', value: 'help' },
  { label: '水漫金山', value: 'chat' },
  { label: '闲置', value: 'idle' },
  { label: '求购', value: 'buy' },
  { label: '悬赏', value: 'reward' },
  { label: '租房', value: 'rent' },
  { label: '帮转', value: 'forward' },
  { label: '寻物招领', value: 'lost-found' },
]

const searchResults = ref([
  {
    title: '校园食堂满意度调查结果公布',
    content: '根据最新调查显示，学生对食堂的满意度达到85%，较去年提升5个百分点...',
    url: '#',
    time: '2024-03-20 10:30',
    sentiment: 'positive',
  },
  {
    title: '图书馆占座问题引发热议',
    content: '近期图书馆占座现象严重，学生反映找不到座位的情况时有发生...',
    url: '#',
    time: '2024-03-20 09:15',
    sentiment: 'negative',
  },
])

const pagination = {
  pageSize: 10,
  total: 100,
  showSizeChanger: true,
  showQuickJumper: true,
}

// AI 总结数据
const aiSummary = ref({
  overview:
    '根据当前筛选条件，共发现 156 条相关讨论，其中正面情感占比 65%，负面情感占比 20%，中性情感占比 15%。主要涉及食堂服务、图书馆管理、校园环境等话题。',
  findings: [
    '食堂服务满意度较上月提升 5%，主要得益于新增的菜品和改善的服务态度',
    '图书馆占座问题引发较多负面情绪，建议加强管理和监督',
    '校园环境改善获得学生普遍好评，特别是新增的绿化区域',
    '学生活动参与度显著提升，反映出校园文化建设的积极成效',
  ],
  suggestions: [
    '建议重点关注图书馆占座问题，可以考虑引入智能预约系统',
    '食堂服务改进效果明显，建议继续保持并推广成功经验',
    '校园环境改善获得好评，建议继续推进相关项目',
    '可以进一步挖掘学生活动成功经验，推广到其他领域',
  ],
})

const onSearch = (value: string) => {
  console.log('搜索:', value)
  console.log('情感筛选:', selectedEmotions.value)
  console.log('主题筛选:', selectedTopics.value)
  console.log('时间范围:', dateRange.value)
  // 这里添加搜索逻辑
}

const refreshSummary = () => {
  summaryLoading.value = true
  // 模拟 AI 生成总结的延迟
  setTimeout(() => {
    summaryLoading.value = false
  }, 1000)
}
</script>

<style scoped>
.ai-search {
  padding: 20px;
}

h1 {
  font-size: 24px;
  margin-bottom: 24px;
}

.search-container {
  max-width: 1200px;
  margin: 0 auto;
}

.search-filters {
  margin-top: 16px;
  margin-bottom: 24px;
  background: #fafafa;
  padding: 24px;
  border-radius: 4px;
}

.ai-summary {
  margin: 24px auto;
  max-width: 1200px;
}

.summary-card {
  background: #fafafa;
}

.summary-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.summary-content {
  padding: 16px 0;
}

.summary-section {
  margin-bottom: 24px;
}

.summary-section:last-child {
  margin-bottom: 0;
}

.summary-section h3 {
  font-size: 16px;
  margin-bottom: 12px;
  color: #1890ff;
}

.summary-section p {
  margin: 0;
  line-height: 1.6;
}

.summary-section ul {
  margin: 0;
  padding-left: 20px;
}

.summary-section li {
  margin-bottom: 8px;
  line-height: 1.6;
}

.search-results {
  margin-top: 24px;
}

.time {
  margin-left: 16px;
  color: #999;
}

:deep(.ant-form-item) {
  margin-bottom: 0;
}
</style>
