<template>
  <div class="warning">
    <h1>异常预警</h1>

    <a-row :gutter="16">
      <a-col :span="24">
        <a-card title="预警概览" :bordered="false">
          <a-row :gutter="16">
            <a-col :span="6">
              <a-statistic title="今日预警" :value="12" :value-style="{ color: '#cf1322' }">
                <template #prefix>
                  <warning-outlined />
                </template>
              </a-statistic>
            </a-col>
            <a-col :span="6">
              <a-statistic title="待处理" :value="5" :value-style="{ color: '#faad14' }">
                <template #prefix>
                  <clock-circle-outlined />
                </template>
              </a-statistic>
            </a-col>
            <a-col :span="6">
              <a-statistic title="已处理" :value="7" :value-style="{ color: '#3f8600' }">
                <template #prefix>
                  <check-circle-outlined />
                </template>
              </a-statistic>
            </a-col>
            <a-col :span="6">
              <a-statistic
                title="平均响应时间"
                value="2.5"
                suffix="小时"
                :value-style="{ color: '#1890ff' }"
              >
                <template #prefix>
                  <field-time-outlined />
                </template>
              </a-statistic>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" style="margin-top: 16px">
      <a-col :span="24">
        <a-card title="预警列表" :bordered="false">
          <a-table :columns="columns" :data-source="data">
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'level'">
                <a-tag :color="getLevelColor(record.level)">
                  {{ record.level }}
                </a-tag>
              </template>
              <template v-if="column.key === 'status'">
                <a-tag :color="getStatusColor(record.status)">
                  {{ record.status }}
                </a-tag>
              </template>
              <template v-if="column.key === 'action'">
                <a-space>
                  <a-button type="link" size="small">查看详情</a-button>
                  <a-button type="link" size="small">处理</a-button>
                </a-space>
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
import {
  WarningOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined,
  FieldTimeOutlined,
} from '@ant-design/icons-vue'

interface TableItem {
  key: string
  title: string
  level: string
  source: string
  time: string
  status: string
}

const columns = [
  {
    title: '预警内容',
    dataIndex: 'title',
    key: 'title',
  },
  {
    title: '预警等级',
    dataIndex: 'level',
    key: 'level',
  },
  {
    title: '来源',
    dataIndex: 'source',
    key: 'source',
  },
  {
    title: '时间',
    dataIndex: 'time',
    key: 'time',
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
  },
  {
    title: '操作',
    key: 'action',
  },
]

const data = ref<TableItem[]>([
  {
    key: '1',
    title: '校园论坛出现大量负面言论',
    level: '高',
    source: '校园论坛',
    time: '2024-03-20 10:30',
    status: '待处理',
  },
  {
    key: '2',
    title: '食堂投诉量突增',
    level: '中',
    source: '投诉系统',
    time: '2024-03-20 09:15',
    status: '处理中',
  },
  {
    key: '3',
    title: '图书馆占座问题引发争议',
    level: '低',
    source: '社交媒体',
    time: '2024-03-20 08:45',
    status: '已处理',
  },
])

const getLevelColor = (level: string) => {
  switch (level) {
    case '高':
      return 'red'
    case '中':
      return 'orange'
    case '低':
      return 'blue'
    default:
      return 'default'
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case '待处理':
      return 'red'
    case '处理中':
      return 'orange'
    case '已处理':
      return 'green'
    default:
      return 'default'
  }
}
</script>

<style scoped>
.warning {
  padding: 20px;
}

h1 {
  font-size: 24px;
  margin-bottom: 24px;
}
</style>
