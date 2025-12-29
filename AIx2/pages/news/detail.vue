<template>
  <view class="page">
    <view class="header">
      <text class="title">{{ preview.title || '资讯详情' }}</text>
      <text class="subtitle">智能概况</text>
    </view>
    <view class="card">
      <text class="summary">{{ preview.summary }}</text>
      <view class="points" v-if="preview.key_points && preview.key_points.length">
        <text class="point" v-for="(point, index) in preview.key_points" :key="index">• {{ point }}</text>
      </view>
      <text class="timestamp">更新时间：{{ preview.fetched_at }}</text>
    </view>

    <view class="source">
      <text class="source-label">来源链接</text>
      <text class="source-url">{{ preview.source_url }}</text>
      <view class="actions">
        <button class="btn" @click="copyLink">复制链接</button>
        <button class="btn primary" @click="openOriginal">打开原文</button>
      </view>
    </view>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  data() {
    return {
      newsId: null,
      sourceUrl: '',
      preview: {
        title: '',
        summary: '',
        key_points: [],
        source_url: '',
        fetched_at: ''
      }
    }
  },
  onLoad(options) {
    this.newsId = options.id || null
    this.sourceUrl = decodeURIComponent(options.url || '')
    this.fetchPreview()
  },
  methods: {
    fetchPreview() {
      if (this.newsId) {
        request({ url: `/api/news/${this.newsId}/preview` })
          .then((res) => {
            this.preview = res || this.preview
          })
          .catch(() => {
            uni.showToast({ title: '获取概况失败', icon: 'none' })
          })
        return
      }
      if (!this.sourceUrl) {
        uni.showToast({ title: '缺少来源链接', icon: 'none' })
        return
      }
      request({ url: '/api/news/preview', method: 'POST', data: { url: this.sourceUrl } })
        .then((res) => {
          this.preview = res || this.preview
        })
        .catch(() => {
          uni.showToast({ title: '获取概况失败', icon: 'none' })
        })
    },
    copyLink() {
      if (!this.preview.source_url) return
      uni.setClipboardData({
        data: this.preview.source_url,
        success: () => {
          uni.showToast({ title: '链接已复制', icon: 'none' })
        }
      })
    },
    openOriginal() {
      if (!this.preview.source_url) {
        uni.showToast({ title: '暂无链接', icon: 'none' })
        return
      }
      uni.navigateTo({ url: `/pages/webview/index?url=${encodeURIComponent(this.preview.source_url)}` })
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
  font-size: 34rpx;
  font-weight: 600;
  color: #1c1d1f;
}
.subtitle {
  display: block;
  margin-top: 8rpx;
  color: #7a7f87;
  font-size: 24rpx;
}
.card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.04);
}
.summary {
  font-size: 28rpx;
  color: #1c1d1f;
  line-height: 1.6;
}
.points {
  margin-top: 16rpx;
}
.point {
  display: block;
  margin-top: 8rpx;
  font-size: 24rpx;
  color: #4b4f56;
}
.timestamp {
  margin-top: 16rpx;
  font-size: 22rpx;
  color: #8b9098;
}
.source {
  margin-top: 24rpx;
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
}
.source-label {
  font-size: 26rpx;
  color: #1c1d1f;
  font-weight: 600;
}
.source-url {
  display: block;
  margin-top: 12rpx;
  font-size: 24rpx;
  color: #2563eb;
  word-break: break-all;
}
.actions {
  margin-top: 16rpx;
  display: flex;
  gap: 16rpx;
}
.btn {
  flex: 1;
  border-radius: 12rpx;
  background: #f3f4f6;
  color: #1c1d1f;
  font-size: 24rpx;
}
.primary {
  background: #1c1d1f;
  color: #fff;
}
</style>
