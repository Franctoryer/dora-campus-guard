import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AISearchView from '../views/AISearchView.vue'
import SentimentView from '../views/SentimentView.vue'
import WarningView from '../views/WarningView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        title: '首页',
      },
    },
    {
      path: '/ai-search',
      name: 'ai-search',
      component: AISearchView,
      meta: {
        title: 'AI 智搜',
      },
    },
    {
      path: '/sentiment',
      name: 'sentiment',
      component: SentimentView,
      meta: {
        title: '情感与主题',
      },
    },
    {
      path: '/warning',
      name: 'warning',
      component: WarningView,
      meta: {
        title: '异常预警',
      },
    },
  ],
})

export default router
