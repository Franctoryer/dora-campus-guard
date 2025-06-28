<template>
  <div class="warning">
    <a-row :gutter="16">
      <a-col :span="24">
        <a-card title="预警概览" :bordered="false">
          <a-row :gutter="16">
            <a-col :span="6">
              <a-statistic title="总预警数" :value="total" :value-style="{ color: '#cf1322' }">
                <template #prefix>
                  <alert-outlined />
                </template>
              </a-statistic>
            </a-col>
            <a-col :span="6">
              <a-statistic title="严重预警" :value="highCount" :value-style="{ color: '#fa541c' }">
                <template #prefix>
                  <fire-outlined />
                </template>
              </a-statistic>
            </a-col>
            <a-col :span="6">
              <a-statistic
                title="中级预警"
                :value="mediumCount"
                :value-style="{ color: '#faad14' }"
              >
                <template #prefix>
                  <exclamation-circle-outlined />
                </template>
              </a-statistic>
            </a-col>
            <a-col :span="6">
              <a-statistic title="低级预警" :value="lowCount" :value-style="{ color: '#3f8600' }">
                <template #prefix>
                  <info-circle-outlined />
                </template>
              </a-statistic>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16" style="margin-top: 16px">
      <a-col :span="24">
        <a-select v-model:value="level" @change="getAbnormalPosts">
          <a-select-option :value="null">全部</a-select-option>
          <a-select-option :value="1">低级预警</a-select-option>
          <a-select-option :value="2">中级预警</a-select-option>
          <a-select-option :value="3">高级预警</a-select-option>
        </a-select>
        <a-list
          :data-source="abnormalPosts"
          v-model:pagination="pagination"
          item-layout="horizontal"
        >
          <template #renderItem="{ item }">
            <a-list-item key="item.id" class="post-info">
              <!-- 用户信息 -->
              <a-list-item-meta class="user-info">
                <template #title>
                  {{ item?.nickname || '无昵称' }}
                  <a-tag color="red" class="level-tag" v-if="item?.isAdmin"> 管理员 </a-tag>
                  <a-tag color="blue" class="level-tag" v-else>{{
                    `Lv.${item?.level || 0}`
                  }}</a-tag>
                </template>
                <template #avatar>
                  <a-avatar :src="item?.avatarUrl || ''" />
                </template>
                <template #description>
                  <span class="time">{{ item.publishedAt }}</span>
                </template>
              </a-list-item-meta>
              <!-- 正文 -->
              <div
                v-html="item.content"
                class="post-content"
                @click="goToPost(item.id)"
                style="cursor: pointer"
              ></div>
              <!-- 额外信息 -->
              <div class="post-extra">
                <a-tag :color="SentimentUtil.getLabelColorFromLabelId(item.sentimentLabel)">{{
                  SentimentUtil.getLabelNameFromLabelId(item.sentimentLabel)
                }}</a-tag>

                <!-- 预警标签 -->
                <a-tag v-if="item.abnormalIndex > 0" :color="getAbnormalColor(item.abnormalIndex)">
                  {{ getAbnormalLabel(item.abnormalIndex) }}
                </a-tag>
              </div>
            </a-list-item>
          </template>
        </a-list>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import {
  AlertOutlined,
  FireOutlined,
  ExclamationCircleOutlined,
  InfoCircleOutlined,
} from '@ant-design/icons-vue'
import service from '@/util/axios'
import SentimentUtil from '@/util/sentimentUtil'

onMounted(() => {
  getDetectionSummary()
  getAbnormalPosts()
})

// ========== 预警总结 =============

const lowCount = ref<number>(0)
const mediumCount = ref<number>(0)
const highCount = ref<number>(0)
const total = computed(() => lowCount.value + mediumCount.value + highCount.value)

const getDetectionSummary = async () => {
  const res = await service.get('/detection/detection-summary')
  lowCount.value = res.data.lowCount
  mediumCount.value = res.data.mediumCount
  highCount.value = res.data.highCount
}

// =========== 获取预警列表 =================
const abnormalPosts = ref([])
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
    getAbnormalPosts()
  },
})
const level = ref(null)
const getAbnormalPosts = async () => {
  const res = await service.get('/detection/abnormal-post-list', {
    params: {
      pageNum: pagination.current,
      pageSize: pagination.pageSize,
      abnormalIndex: level.value,
    },
  })
  abnormalPosts.value = res.data.records
}

const getAbnormalLabel = (index: number) => {
  switch (index) {
    case 3:
      return '高级预警'
    case 2:
      return '中级预警'
    case 1:
      return '低级预警'
    default:
      return ''
  }
}

const getAbnormalColor = (index: number) => {
  switch (index) {
    case 3:
      return 'red'
    case 2:
      return 'orange'
    case 1:
      return 'green'
    default:
      return ''
  }
}

// ============== 页面跳转 ================
const goToPost = (id: number) => {
  window.open(`https://a.ktllq.cn/${id}`, '_blank')
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
</style>
