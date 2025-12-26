<template>
  <view class="page">
    <view class="header">
      <text class="title">资讯</text>
      <text class="subtitle">关注你关心的内容</text>
    </view>
    <view class="actions">
      <button class="ghost" @click="goArchive">归档查询</button>
    </view>
    <view class="card" v-for="item in items" :key="item.id" @click="openDetail(item)">
      <text class="card-title">{{ item.title }}</text>
      <text class="card-summary">{{ item.summary }}</text>
      <view class="card-meta">
        <text>{{ item.source }}</text>
        <text>{{ item.published_at }}</text>
      </view>
    </view>
    <view class="empty" v-if="items.length === 0">
      <text>暂无资讯，请稍后再试</text>
    </view>
    <button v-if="hasMore" class="load-more" @click="loadMore">加载更多</button>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  data() {
    return {
      items: [],
      page: 1,
      hasMore: false,
      loading: false
    }
  },
  onShow() {
    this.page = 1
    this.items = []
    this.fetchNews()
  },
  methods: {
    fetchNews() {
      if (this.loading) return
      this.loading = true
      request({ url: `/api/news?page=${this.page}&page_size=10` })
        .then((res) => {
          const nextItems = res.items || []
          this.items = this.items.concat(nextItems)
          this.hasMore = res.has_more
        })
        .catch(() => {
          uni.showToast({ title: '资讯获取失败', icon: 'none' })
        })
        .finally(() => {
          this.loading = false
        })
    },
    loadMore() {
      if (!this.hasMore) return
      this.page += 1
      this.fetchNews()
    },
    openDetail(item) {
      if (!item) return
      const url = item.url ? encodeURIComponent(item.url) : ''
      uni.navigateTo({ url: `/pages/news/detail?id=${item.id || ''}&url=${url}` })
    },
    goArchive() {
      uni.navigateTo({ url: '/pages/news/archive' })
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
.actions {
  margin-bottom: 20rpx;
}
.ghost {
  background: #fff;
  color: #1c1d1f;
  border: 1rpx solid #e5e7eb;
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
</style>
