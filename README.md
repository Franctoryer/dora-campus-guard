# 哆啦哨兵 · Dora Campus Guard 🛡️

一个面向 **校园交流平台（哆啦校圈）** 的 **智能舆情分析与搜索平台**。  
融合 **爬虫实时采集、NLP 情感分析、RAG 检索增强、异常预警** 等多种 AI 技术，  
致力于让高校舆情分析变得 **高效 · 智能 · 可视化 · 有温度** ✨。

[![GitHub stars](https://img.shields.io/github/stars/Franctoryer/dora-campus-guard?style=social)](https://github.com/Franctoryer/dora-campus-guard)
[![GitHub forks](https://img.shields.io/github/forks/Franctoryer/dora-campus-guard?style=social)](https://github.com/Franctoryer/dora-campus-guard)

---

## 🌟 项目特色亮点

- **真实数据驱动**：基于哆啦校圈真实语料，累计抓取 `50w+` 帖子与用户数据。
- **AI 智搜**：支持 **关键词检索 + 语义搜索 + AI 摘要**，  
  不仅能查，还能秒懂。
- **细粒度情感识别**：RoBERTa 微调，支持 **7 类情绪标签**（悲伤 / 失望 / 讨厌 / 平和 / 疑惑 / 开心 / 期待），准确率 81%+。
- **异常预警机制**：融合 **情感倾向 + 敏感词 + 举报数**，实现低/中/高三级风险预警，日均拦截 `50+` 可疑帖子。
- **RAG 检索增强**：检索 + 大模型结合，生成有理有据的总结与回答。
- **多维可视化分析**：词云、趋势图、情绪分布、风险图表，一图看懂校园动态。
- **高性能架构**：生产者-消费者解耦，全链路耗时 `<200ms`，保证实时性与一致性。
- **Docker 容器化**：一键启动，支持快速部署与扩展。

---

## 🖼️ 功能展示

### 🔍 AI 智搜
- 关键词联想 + 语义检索
- 自动生成 AI 摘要
- 情绪趋势与热度走势可视化

### 📊 主题与情感
- 今日热点词云图
- 情绪趋势折线图
- 热门话题分布统计

### 🚨 异常预警
- 多级预警（低/中/高）
- 异常帖子列表（筛选查看）
- 实时风险概览面板

---

## 🏗️ 系统架构

```
爬虫系统 (Scrapy) → RabbitMQ → 消费者 (NLP/检测服务)
│ │
▼ ▼
MySQL ← 双写策略 → ElasticSearch ←→ RAG Summarizer
```


- **前端**：Vue 3 + TypeScript + Ant Design Vue + Pinia  
- **后端**：Spring Boot + MyBatis-Plus + XML-RPC  
- **爬虫**：Python + Scrapy（突破加密、滑块、点选验证码，识别准确率 90%+）  
- **消息队列**：RabbitMQ（延时 + 死信队列，消息丢失率≈0）  
- **数据库**：MySQL（事务性数据）+ ElasticSearch（检索与聚合）  
- **AI 模型**：RoBERTa 中文预训练模型微调，支持 7 类情感分类  
- **部署**：Docker / Docker Compose（统一环境管理，一键启动）

---

## 🧠 技术细节

### 🔹 情感分类模型
- 输入：用户发帖文本  
- 输出：7 类情绪标签（含置信度分值）  
- 存储：`sentiment_label` + `sentiment_confidence`

### 🔹 异常检测算法
- 情感预筛选（仅负面情绪进入检测）  
- 敏感词匹配（黑/白名单）  
- 举报信息加权  
- 风险评分 → 0（正常）~ 3（高级预警）

### 🔹 RAG 检索增强
1. 用户查询 → 构建 ES 检索请求  
2. 获取 Top-K 相关帖子 → 注入大模型  
3. 生成上下文相关、可追溯的智能摘要  

---

## 📂 数据库设计（核心表）

- **posts**：帖子表（正文、情绪标签、风险指数等）  
- **users**：用户表（头像、等级、举报状态等）  
- **spider_records**：爬虫任务记录表（运行状态、日志摘要等）  

---

## 🚀 快速启动

```bash
# 克隆项目
git clone https://github.com/Franctoryer/dora-campus-guard.git
cd dora-campus-guard

# 启动服务（需安装 Docker & Docker Compose）
docker-compose up -d
