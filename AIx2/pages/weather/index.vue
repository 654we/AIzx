<template>
  <view class="page">
    <view class="header">
      <view>
        <text class="location">{{ locationName }}</text>
        <text class="updated">更新于 {{ updatedAt }}</text>
      </view>
      <text class="temp">{{ temp }}</text>
    </view>

    <view class="card weather-card">
      <text class="condition">{{ condition }}</text>
      <view class="meta">
        <text>湿度 {{ humidity }}%</text>
        <text>风力 {{ wind }}</text>
      </view>
    </view>

    <view class="card">
      <text class="section-title">空气质量</text>
      <view class="meta">
        <text>空气指数 {{ aqi }}（{{ aqiDesc }}）</text>
      </view>
    </view>

    <view class="card">
      <text class="section-title">出行建议</text>
      <view class="tips">
        <text v-for="(tip, index) in tips" :key="index">{{ tip }}</text>
      </view>
    </view>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  data() {
    return {
      locationName: '请选择位置',
      updatedAt: '--:--',
      temp: '--°',
      condition: '--',
      humidity: '--',
      wind: '--',
      aqi: '--',
      aqiDesc: '--',
      tips: ['请先设置位置']
    }
  },
  onShow() {
    const saved = uni.getStorageSync('location')
    if (!saved) {
      this.locationName = '未设置位置'
      this.tips = ['请前往“我的 > 位置设置”更新位置']
      return
    }
    this.loadWeather(saved)
  },
  methods: {
    loadWeather(location) {
      request({ url: `/api/weather?location=${encodeURIComponent(location)}` })
        .then((res) => {
          this.locationName = res.location.name
          this.updatedAt = res.weather.updated_at || '--:--'
          this.temp = `${res.weather.temp_c}°`
          this.condition = res.weather.condition
          this.humidity = res.weather.humidity
          this.wind = res.weather.wind
          this.aqi = res.weather.aqi
          this.aqiDesc = res.weather.aqi_desc
          this.tips = res.travel_advice.length ? res.travel_advice : ['天气舒适，适合出行。']
        })
        .catch(() => {
          this.tips = ['天气获取失败，请稍后重试']
          uni.showToast({ title: '天气获取失败', icon: 'none' })
        })
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24rpx;
}
.location {
  font-size: 32rpx;
  font-weight: 600;
  color: #1c1d1f;
}
.updated {
  display: block;
  margin-top: 8rpx;
  font-size: 24rpx;
  color: #7a7f87;
}
.temp {
  font-size: 64rpx;
  font-weight: 600;
  color: #1c1d1f;
}
.card {
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.04);
}
.weather-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.condition {
  font-size: 30rpx;
  font-weight: 600;
}
.meta {
  display: flex;
  justify-content: space-between;
  margin-top: 12rpx;
  color: #7a7f87;
  font-size: 24rpx;
}
.section-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #1c1d1f;
}
.tips text {
  display: block;
  margin-top: 12rpx;
  font-size: 24rpx;
  color: #4b4f56;
}
</style>
