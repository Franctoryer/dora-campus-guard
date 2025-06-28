<template>
  <div class="ai-search">
    <div class="search-container">
      <a-input-search
        v-model:value="searchText"
        placeholder="输入关键词进行智能搜索"
        enter-button
        size="large"
        @search="searchKeyword"
      >
        <template #prefix>
          <robot-outlined />
        </template>
      </a-input-search>

      <div class="filter-and-ai">
        <div class="filter">
          <a-col>
            <a-divider orientation="left">情感类型</a-divider>
            <a-radio-group
              v-model:value="selectedEmotion"
              button-style="solid"
              @change="getSearchResult"
            >
              <a-radio-button v-for="item in emotionOptions" :key="item.label" :value="item.value">
                {{ item.label }}
              </a-radio-button>
            </a-radio-group>
          </a-col>
          <a-col>
            <a-divider orientation="left">主题类型</a-divider>
            <a-select
              v-model:value="selectedTopic"
              :options="topicOptions"
              style="width: 100%"
              placeholder="请选择您的主题类型"
              @change="getSearchResult"
            ></a-select>
          </a-col>
          <a-col>
            <a-divider orientation="left">时间范围</a-divider>
            <a-range-picker
              v-model:value="dateRange"
              style="width: 100%"
              :show-time="{ format: 'HH:mm' }"
              format="YYYY-MM-DD HH:mm"
              :placeholder="['开始时间', '结束时间']"
            ></a-range-picker>
          </a-col>
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
                {{ summaryContent || '我是您的 AI 助手，快速生成舆情总结' }}
              </a-spin>
            </div>
          </a-card>
        </div>
      </div>
    </div>
    <div class="two-charts">
      <div class="sentiment-distribution">
        <v-chart class="chart" :option="sentimentDistributionPieOption" autoresize />
      </div>
      <div class="keyword-trend">
        <a-select v-model:value="interval" @change="getKeywordTrend">
          <a-select-option value="day">按天</a-select-option>
          <a-select-option value="month">按月</a-select-option>
          <a-select-option value="year">按年</a-select-option>
        </a-select>
        <v-chart class="chart" :option="keywordTrendOption" autoresize />
      </div>
    </div>
    <div class="search-results" v-if="searchResults.length">
      <a-divider orientation="left"
        >总共 <b>{{ pagination.total }}</b> 条搜索记录</a-divider
      >
      <a-list :data-source="searchResults" v-model:pagination="pagination" item-layout="horizontal">
        <template #renderItem="{ item }">
          <a-list-item key="item.id" class="post-info">
            <!-- 用户信息 -->
            <a-list-item-meta class="user-info">
              <template #title>
                {{ item?.user?.nickname || '无昵称' }}
                <a-tag color="red" class="level-tag" v-if="item.user?.isAdmin"> 管理员 </a-tag>
                <a-tag color="blue" class="level-tag" v-else>{{
                  `Lv.${item.user?.level || 0}`
                }}</a-tag>
              </template>
              <template #avatar>
                <a-avatar :src="item.user?.avatarUrl || ''" />
              </template>
              <template #description>
                <span class="time">{{ item.post.publishedAt }}</span>
              </template>
            </a-list-item-meta>
            <!-- 正文 -->
            <div
              v-html="item.post.content"
              class="post-content"
              @click="goToPost(item.post.id)"
              style="cursor: pointer"
            ></div>
            <!-- 额外信息 -->
            <div class="post-extra">
              <a-space wrap class="post-meta-icons">
                <a-tooltip title="点赞">
                  <span class="meta-icon like">
                    <like-outlined />
                    {{ item.post.likeSum }}
                  </span>
                </a-tooltip>

                <a-tooltip title="评论">
                  <span class="meta-icon comment">
                    <message-outlined />
                    {{ item.post.commentSum }}
                  </span>
                </a-tooltip>

                <a-tooltip title="蹲贴（关注）">
                  <span class="meta-icon wait">
                    <clock-circle-outlined />
                    {{ item.post.dunNum }}
                  </span>
                </a-tooltip>

                <a-tooltip title="举报">
                  <span class="meta-icon report">
                    <warning-outlined />
                    {{ item.post.tipSum }}
                  </span>
                </a-tooltip>
              </a-space>
              <a-tag :color="SentimentUtil.getLabelColorFromLabelId(item.post.sentimentLabel)">{{
                SentimentUtil.getLabelNameFromLabelId(item.post.sentimentLabel)
              }}</a-tag>
            </div>
          </a-list-item>
        </template>
      </a-list>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { RobotOutlined, ReloadOutlined } from '@ant-design/icons-vue'
import type { Dayjs } from 'dayjs'
import service from '@/util/axios'
import SentimentUtil from '@/util/sentimentUtil'
import {
  LikeOutlined,
  MessageOutlined,
  ClockCircleOutlined,
  WarningOutlined,
} from '@ant-design/icons-vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  ToolboxComponent,
} from 'echarts/components'
import type { keywordTrend, SentimentDistribution } from '@/types/sentiment'

// 注册 ECharts 组件
use([
  CanvasRenderer,
  PieChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  ToolboxComponent,
  LegendComponent,
  GridComponent,
])

const searchText = ref('')
const selectedEmotion = ref<number>(-1)
const selectedTopic = ref<number>(-1)
const dateRange = ref<[Dayjs, Dayjs] | null>(null)
const startTime = computed(() =>
  dateRange.value?.length && dateRange.value.length > 0
    ? dateRange.value[0].format('YYYY-MM-DDTHH:mm:ss')
    : null,
)
const endTime = computed(() =>
  dateRange.value?.length && dateRange.value.length > 1
    ? dateRange.value[1].format('YYYY-MM-DDTHH:mm:ss')
    : null,
)
const pagination = reactive({
  current: 1,
  pageSize: 20,
  total: 0,
  showSizeChanger: true,
  // showQuickJumper: true,
  pageSizeOptions: ['10', '20', '30', '40'],
  onChange: (page: number, pageSize: number) => {
    pagination.current = page
    pagination.pageSize = pageSize
    getSearchResult()
  },
})
const summaryLoading = ref(false)
// 查询结果
const searchResults = ref([])

// 页面挂载回调
onMounted(async () => {
  // 获取帖子列表
  getSearchResult()
  getSearchSentimentDistribution()
  getKeywordTrend()
})

const emotionOptions = [
  { label: '全部', value: -1 },
  { label: '悲伤', value: 0 },
  { label: '失望', value: 1 },
  { label: '讨厌', value: 2 },
  { label: '平和', value: 3 },
  { label: '疑惑', value: 4 },
  { label: '开心', value: 5 },
  { label: '期待', value: 6 },
]

const topicOptions = [
  { label: '全部', value: -1 },
  { label: '投稿', value: 1 },
  { label: '求助', value: 2 },
  { label: '水漫金山', value: 24 },
  { label: '闲置', value: 3 },
  { label: '求购', value: 15 },
  { label: '悬赏', value: 14 },
  { label: '租房', value: 4 },
  { label: '帮转', value: 5 },
  { label: '找人', value: 7 },
  { label: '寻物招领', value: 8 },
  { label: '公告', value: 9 },
  { label: '求问', value: 11 },
  { label: '卖室友', value: 12 },
  { label: '选课交流', value: 13 },
]

/**
 * 查询了某个关键词
 */
const searchKeyword = () => {
  // 将页码置为 1
  pagination.current = 1
  // 获取查询结果
  getSearchResult()
  // 获取情感分布
  getSearchSentimentDistribution()
  // 获取讨论趋势
  getKeywordTrend()
  // 生成 AI 总结
  refreshSummary()
}

/**
 * 获取查询结果
 */
const getSearchResult = async () => {
  try {
    const res = await service.get('/post/search', {
      params: {
        keyword: searchText.value,
        sentimentLabel: selectedEmotion.value == -1 ? null : selectedEmotion.value,
        topicId: selectedTopic.value == -1 ? null : selectedTopic.value,
        page: pagination.current - 1,
        size: pagination.pageSize,
        startTime: startTime.value,
        endTime: endTime.value,
      },
    })

    searchResults.value = res.data.content
    // 文档总数
    pagination.total = res.data.totalElements
  } catch {
    alert('获取数据失败')
  }
}

// ================= AI 总结 =====================

const summaryContent = ref<string>('')
const refreshSummary = () => {
  summaryLoading.value = true
  summaryContent.value = ''
  const eventSource = new EventSource(
    `http://127.0.0.1:8080/rest/post/search-summary?keyword=${searchText.value}`,
  )

  eventSource.onmessage = (event) => {
    summaryLoading.value = false
    if (event.data === '[DONE]') {
      eventSource.close()
    } else {
      const jsonData = JSON.parse(event.data)
      const data = jsonData['choices'][0]['delta']['content']
      summaryContent.value += data
    }
  }
}

// =============== 画情感分布饼图 ====================
// 响应数据
const sentimentDistributionData = ref<SentimentDistribution[]>([])
// 展示数据
const sentimentDistributionDisplayData = computed(() => {
  const original = sentimentDistributionData.value.map((item) => ({
    name: item.labelName,
    value: item.count,
  }))

  const desiredOrder = ['悲伤', '失望', '讨厌', '平和', '疑惑', '开心', '期待']

  // 排序
  return desiredOrder.map((name) => original.find((item) => item.name === name)).filter(Boolean) // 去掉找不到的
})

/**
 * 获取查询结果的情感分布
 */
const getSearchSentimentDistribution = async () => {
  const res = await service.get('/post/sentiment-distribution', {
    params: {
      keyword: searchText.value,
      topicId: selectedTopic.value == -1 ? null : selectedTopic.value,
      startTime: startTime.value,
      endTime: endTime.value,
    },
  })
  // 获取情感分布数据
  sentimentDistributionData.value = res.data
}

// Echarts 图表配置
const sentimentDistributionPieOption = computed(() => {
  const data = sentimentDistributionDisplayData.value

  // 聚合为主类分布
  const groupMap = {
    消极: ['悲伤', '失望', '讨厌'],
    中性: ['平和', '疑惑'],
    积极: ['开心', '期待'],
  }

  const mainCategoryCount = {
    消极: 0,
    中性: 0,
    积极: 0,
  }

  data.forEach((item) => {
    for (const [mainCategory, subLabels] of Object.entries(groupMap)) {
      if (!item) continue
      if (subLabels.includes(item.name)) {
        // @ts-ignore
        mainCategoryCount[mainCategory] += item.value
        break
      }
    }
  })

  const innerData = Object.entries(mainCategoryCount).map(([name, value]) => ({
    name,
    value,
  }))
  return {
    title: {
      text: '大众情绪',
      subtext: searchText.value,
      left: 'center',
    },
    tooltip: {
      trigger: 'item',
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    toolbox: {
      right: 10,
      feature: {
        dataZoom: {
          yAxisIndex: 'none',
        },
        restore: {},
        saveAsImage: {},
      },
    },
    series: [
      {
        name: '主类',
        type: 'pie',
        selectedMode: 'single',
        radius: [0, '50%'], // 内圈
        label: {
          position: 'inner',
          fontSize: 12,
        },
        data: innerData,
      },
      {
        name: '细分类',
        type: 'pie',
        radius: ['50%', '70%'], // 外圈
        label: {
          formatter: '{b} ({d}%)',
        },
        data: data,
      },
    ],
  }
})

// ================ 画讨论趋势折线图 ===================
// 关键词随时间的热度数据
const keywordTrendData = ref<keywordTrend[]>([])
const interval = ref('day')
// 获取趋势数据
const getKeywordTrend = async () => {
  const res = await service.get('/post/keyword-trend', {
    params: {
      keyword: searchText.value,
      startTime: startTime.value,
      endTime: endTime.value,
      interval: interval.value,
    },
  })
  // 获取情感分布数据
  keywordTrendData.value = res.data
}
// 折线图配置
const keywordTrendOption = computed(() => {
  return {
    title: {
      text: '讨论趋势',
      left: 'center',
      textStyle: {
        fontSize: 18,
        fontWeight: 'bold',
      },
    },
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br/>热度: {c}',
    },
    toolbox: {
      right: 10,
      feature: {
        dataZoom: {
          yAxisIndex: 'none',
        },
        restore: {},
        saveAsImage: {},
      },
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: keywordTrendData.value.map((item) => item.dateTime),
      axisLabel: {
        rotate: 45,
      },
    },
    yAxis: {
      type: 'value',
      minInterval: 1,
      splitLine: {
        lineStyle: {
          type: 'dashed',
        },
      },
    },
    series: [
      {
        name: '热度',
        type: 'line',
        smooth: true,
        showSymbol: true,
        symbolSize: 6,
        data: keywordTrendData.value.map((item) => item.count),
        lineStyle: {
          width: 3,
          color: '#1890ff',
        },
        itemStyle: {
          color: '#1890ff',
          borderColor: '#fff',
          borderWidth: 2,
        },
        areaStyle: {
          color: 'rgba(24, 144, 255, 0.2)',
        },
      },
    ],
    grid: {
      left: '3%',
      right: '4%',
      bottom: '12%',
      containLabel: true,
    },
  }
})

// ============== 页面跳转 ================
const goToPost = (id: number) => {
  window.open(`https://a.ktllq.cn/${id}`, '_blank')
}
</script>

<style scoped>
::v-deep(.keyword) {
  color: rgb(211, 7, 7);
  font-weight: bold;
}

.filter-and-ai {
  display: flex;
  flex-direction: row;
  gap: 40px;
}

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

.filter {
  flex: 3;
}

.ai-summary {
  margin: auto;
  flex: 4;
  height: 100%;
  margin-top: 30px;
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
  padding: 10px 0;
}

.summary-section {
  margin-bottom: 24px;
}

.time {
  color: #999;
}

:deep(.ant-form-item) {
  margin-bottom: 0;
}

.search-results {
  max-width: 1200px;
  margin: auto;
  margin-top: 20px;
}

.user-info {
  flex: 1;
}

.post-content {
  padding: 20px;
  flex: 3;
}

.post-extra {
  flex: 1;
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 14px;
  justify-content: center;
  align-items: center;
}

.post-extra .tag {
  background: #f0f0f0;
  border-radius: 4px;
  padding: 2px 6px;
  font-weight: 500;
}

.post-info {
  display: flex;
  flex-direction: row;
  gap: 10px;
}

.post-meta-icons {
  margin-top: 8px;
  font-size: 14px;
  color: #666;
  gap: 16px;
}

.meta-icon {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.meta-icon.like {
  color: #1677ff;
}

.meta-icon.comment {
  color: #52c41a;
}

.meta-icon.wait {
  color: #faad14;
}

.meta-icon.report {
  color: #ff4d4f;
}

.level-tag {
  margin-left: 5px;
}

.chart {
  height: 100%;
  width: 100%;
}

.sentiment-distribution {
  width: 50%;
  height: 450px;
  margin: auto;
  margin-top: 20px;
}

.keyword-trend {
  width: 50%;
  height: 450px;
  margin: auto;
  margin-top: 20px;
}

.two-charts {
  display: flex;
  flex-direction: row;
  margin: auto;
  margin-top: 20px;
}
</style>
