<template>
  <div class="sentiment">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card title="热门话题词云" :bordered="false">
          <div class="chart-container">
            <v-chart class="chart" :option="wordCloudOption" autoresize />
          </div>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" style="margin-top: 16px">
      <a-col :span="16">
        <a-card title="情感趋势" :bordered="false">
          <div class="chart-container">
            <v-chart class="chart" :option="trendOption" autoresize />
          </div>
        </a-card>
      </a-col>

      <a-col :span="8">
        <a-card title="情感分布" :bordered="false">
          <div class="chart-container">
            <v-chart class="chart" :option="pieOption" autoresize />
          </div>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" style="margin-top: 16px">
      <a-col :span="24">
        <a-card title="热门主题" :bordered="false">
          <a-table :columns="columns" :data-source="data" :pagination="false">
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'sentiment'">
                <a-tag
                  :color="
                    record.sentiment === 'positive'
                      ? 'green'
                      : record.sentiment === 'negative'
                        ? 'red'
                        : 'blue'
                  "
                >
                  {{
                    record.sentiment === 'positive'
                      ? '正面'
                      : record.sentiment === 'negative'
                        ? '负面'
                        : '中性'
                  }}
                </a-tag>
              </template>
              <template v-if="column.key === 'trend'">
                <span :style="{ color: record.trend === 'up' ? '#52c41a' : '#f5222d' }">
                  {{ record.trend === 'up' ? '↑' : '↓' }} {{ record.trendValue }}%
                </span>
              </template>
            </template>
          </a-table>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components'
import 'echarts-wordcloud'

// 注册 ECharts 组件
use([
  CanvasRenderer,
  PieChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
])

// 词云图数据
const wordCloudData = [
  { name: '食堂', value: 1000 },
  { name: '图书馆', value: 800 },
  { name: '宿舍', value: 700 },
  { name: '课程', value: 600 },
  { name: '考试', value: 500 },
  { name: '社团', value: 450 },
  { name: '活动', value: 400 },
  { name: '校园网', value: 350 },
  { name: '空调', value: 300 },
  { name: '热水', value: 280 },
  { name: '占座', value: 260 },
  { name: '作业', value: 240 },
  { name: '教材', value: 220 },
  { name: '早八', value: 200 },
  { name: '门禁', value: 180 },
  { name: '噪音', value: 160 },
  { name: 'Wi-Fi', value: 150 },
  { name: '打印', value: 140 },
  { name: '空教室', value: 130 },
  { name: '排队', value: 120 },
  { name: '开水', value: 110 },
  { name: '答疑', value: 100 },
  { name: '补考', value: 90 },
  { name: '抢课', value: 85 },
  { name: '兼职', value: 80 },
  { name: '社牛', value: 75 },
  { name: '转专业', value: 70 },
  { name: '绩点', value: 65 },
  { name: '挂科', value: 60 },
  { name: '讲座', value: 55 },
  { name: '考研', value: 50 },
  { name: '交换生', value: 45 },
  { name: '保研', value: 40 },
  { name: '志愿', value: 35 },
  { name: '竞赛', value: 30 },
  { name: '奖学金', value: 28 },
  { name: '失物招领', value: 26 },
  { name: '迎新', value: 24 },
  { name: '搬寝', value: 22 },
  { name: '快递', value: 20 },
  { name: '电动车', value: 18 },
  { name: '天气', value: 16 },
  { name: '食物中毒', value: 14 },
  { name: '夜宵', value: 12 },
  { name: '升旗', value: 10 },
  { name: '校园卡', value: 8 },
  { name: '跳蚤市场', value: 6 },
  { name: '水逆', value: 4 },
  { name: '脱单', value: 2 },
]

// 词云图配置
const wordCloudOption = ref({
  tooltip: {
    show: true,
  },
  series: [
    {
      type: 'wordCloud',
      shape: 'circle',
      left: 'center',
      top: 'center',
      width: '90%',
      height: '90%',
      right: null,
      bottom: null,
      sizeRange: [60, 120],
      rotationRange: [-90, 90],
      rotationStep: 45,
      gridSize: 8,
      drawOutOfBound: false,
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: function () {
          return (
            'rgb(' +
            [
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160),
            ].join(',') +
            ')'
          )
        },
      },
      emphasis: {
        focus: 'self',
        textStyle: {
          shadowBlur: 10,
          shadowColor: '#333',
        },
      },
      data: wordCloudData,
    },
  ],
})

// 情感趋势数据
const trendData = {
  dates: ['3-14', '3-15', '3-16', '3-17', '3-18', '3-19', '3-20'],
  positive: [65, 68, 70, 72, 75, 73, 78],
  negative: [20, 18, 15, 17, 14, 16, 12],
  neutral: [15, 14, 15, 11, 11, 11, 10],
}

// 情感趋势图配置
const trendOption = ref({
  tooltip: {
    trigger: 'axis',
  },
  legend: {
    data: ['正面', '负面', '中性'],
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true,
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: trendData.dates,
  },
  yAxis: {
    type: 'value',
    axisLabel: {
      formatter: '{value}%',
    },
  },
  series: [
    {
      name: '正面',
      type: 'line',
      data: trendData.positive,
      smooth: true,
      lineStyle: {
        color: '#52c41a',
      },
      itemStyle: {
        color: '#52c41a',
      },
    },
    {
      name: '负面',
      type: 'line',
      data: trendData.negative,
      smooth: true,
      lineStyle: {
        color: '#f5222d',
      },
      itemStyle: {
        color: '#f5222d',
      },
    },
    {
      name: '中性',
      type: 'line',
      data: trendData.neutral,
      smooth: true,
      lineStyle: {
        color: '#1890ff',
      },
      itemStyle: {
        color: '#1890ff',
      },
    },
  ],
})

// 情感分布数据
const pieData = [
  { value: 65, name: '正面' },
  { value: 20, name: '负面' },
  { value: 15, name: '中性' },
]

// 情感分布图配置
const pieOption = ref({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c}%',
  },
  legend: {
    orient: 'vertical',
    left: 'left',
  },
  series: [
    {
      name: '情感分布',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2,
      },
      label: {
        show: false,
        position: 'center',
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '20',
          fontWeight: 'bold',
        },
      },
      labelLine: {
        show: false,
      },
      data: pieData,
      color: ['#52c41a', '#f5222d', '#1890ff'],
    },
  ],
})

interface TableItem {
  key: string
  topic: string
  mentions: number
  sentiment: 'positive' | 'negative' | 'neutral'
  trend: 'up' | 'down'
  trendValue: number
}

const columns = [
  {
    title: '主题',
    dataIndex: 'topic',
    key: 'topic',
  },
  {
    title: '提及次数',
    dataIndex: 'mentions',
    key: 'mentions',
    sorter: (a: TableItem, b: TableItem) => a.mentions - b.mentions,
  },
  {
    title: '情感倾向',
    dataIndex: 'sentiment',
    key: 'sentiment',
  },
  {
    title: '趋势',
    dataIndex: 'trend',
    key: 'trend',
  },
]

const data = ref<TableItem[]>([
  {
    key: '1',
    topic: '食堂服务',
    mentions: 256,
    sentiment: 'positive',
    trend: 'up',
    trendValue: 15,
  },
  {
    key: '2',
    topic: '图书馆占座',
    mentions: 189,
    sentiment: 'negative',
    trend: 'up',
    trendValue: 8,
  },
  {
    key: '3',
    topic: '校园环境',
    mentions: 145,
    sentiment: 'positive',
    trend: 'down',
    trendValue: 5,
  },
])
</script>

<style scoped>
.sentiment {
  padding: 20px;
}

h1 {
  font-size: 24px;
  margin-bottom: 24px;
}

.chart-container {
  height: 400px;
  width: 100%;
}

.chart {
  height: 100%;
  width: 100%;
}
</style>
