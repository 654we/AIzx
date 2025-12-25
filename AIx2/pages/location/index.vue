<template>
  <view class="page">
    <view class="header">
      <text class="title">位置设置</text>
      <text class="subtitle">用于天气与出行提示</text>
    </view>

    <view class="card">
      <input class="input" type="text" v-model="location" placeholder="输入城市名称，如：上海" />
      <button class="primary" @click="saveLocation">保存位置</button>
    </view>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  data() {
    return {
      location: ''
    }
  },
  onShow() {
    this.location = uni.getStorageSync('location') || ''
  },
  methods: {
    saveLocation() {
      if (!this.location) {
        uni.showToast({ title: '请输入城市名称', icon: 'none' })
        return
      }
      uni.setStorageSync('location', this.location)
      request({
        url: '/api/user/location',
        method: 'PUT',
        data: { location: this.location }
      }).catch(() => {})
      uni.showToast({ title: '位置已更新', icon: 'none' })
      setTimeout(() => {
        uni.navigateBack({ delta: 1 })
      }, 800)
    }
  }
}
</script>

<style scoped>
.page {
  padding: 32rpx;
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
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.04);
}
.input {
  background: #f5f6f8;
  border-radius: 12rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
  font-size: 28rpx;
}
.primary {
  background: #1c1d1f;
  color: #fff;
  border: none;
}
</style>
