<template>
  <view class="page">
    <view class="header">
      <text class="title">归档资讯</text>
      <text class="subtitle">按周查询历史资讯</text>
    </view>
    <view class="card">
      <picker mode="selector" :range="weeks" @change="onWeekChange">
        <view class="picker">{{ selectedWeek || '选择归档周' }}</view>
      </picker>
      <button class="primary" @click="fetchArchive">手动拉取</button>
    </view>
    <view v-if="errorMessage" class="error">{{ errorMessage }}</view>
    <view class="card" v-for="item in items" :key="item.id">
      <text class="card-title">{{ item.title }}</text>
      <text class="card-summary">{{ item.summary }}</text>
      <view class="card-meta">
        <text>{{ item.source }}</text>
        <text>{{ item.published_at }}</text>
      </view>
    </view>
    <view class="empty" v-if="items.length === 0 && !errorMessage">
      <text>暂无归档资讯</text>
    </view>
    <button v-if="hasMore" class="load-more" @click="loadMore">加载更多</button>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  data() {
    return {
      weeks: [],
      selectedWeek: '',
      items: [],
      page: 1,
      hasMore: false,
      errorMessage: ''
    }
  },
  onShow() {
    this.loadWeeks()
  },
  methods: {
    loadWeeks() {
      request({ url: '/api/archive/weeks' })
        .then((res) => {
          this.weeks = res.weeks || []
          this.selectedWeek = res.default || ''
        })
        .catch((err) => {
          this.errorMessage = err?.detail || '归档库未配置或拉取失败'
        })
    },
    onWeekChange(event) {
      const index = event.detail.value
      this.selectedWeek = this.weeks[index]
    },
    fetchArchive() {
      if (!this.selectedWeek) {
        uni.showToast({ title: '请选择归档周', icon: 'none' })
        return
      }
      this.page = 1
      this.items = []
      this.errorMessage = ''
      this.loadArchive()
    },
    loadArchive() {
      request({ url: `/api/archive/news?week=${this.selectedWeek}&page=${this.page}&page_size=10` })
        .then((res) => {
          this.items = this.items.concat(res.items || [])
          this.hasMore = res.has_more
        })
        .catch((err) => {
          this.errorMessage = err?.detail || '归档拉取失败'
        })
    },
    loadMore() {
      if (!this.hasMore) return
      this.page += 1
      this.loadArchive()
    }
  }
}
</script>

<style scoped>
.page {
  padding: 24rpx;
  background-color: #f5f6f8;
  min-height: 100vh;
}
.header {
  margin-bottom: 24rpx;
}
.title {
  font-size: 36rpx;
  font-weight: 600;
  color: #1c1d1f;
}
.subtitle {
  display: block;
  margin-top: 8rpx;
  color: #7a7f87;
  font-size: 26rpx;
}
.card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.04);
}
.picker {
  padding: 16rpx;
  border: 1rpx solid #e5e7eb;
  border-radius: 12rpx;
  margin-bottom: 16rpx;
}
.primary {
  background: #1c1d1f;
  color: #fff;
  border: none;
}
.card-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #1c1d1f;
}
.card-summary {
  display: block;
  margin-top: 12rpx;
  font-size: 26rpx;
  color: #4b4f56;
}
.card-meta {
  margin-top: 16rpx;
  display: flex;
  justify-content: space-between;
  font-size: 22rpx;
  color: #8b9098;
}
.empty {
  text-align: center;
  color: #8b9098;
  margin-top: 80rpx;
}
.load-more {
  margin-top: 16rpx;
  background: #fff;
  border: none;
  color: #1c1d1f;
}
.error {
  margin-bottom: 16rpx;
  color: #d92d20;
}
</style>
