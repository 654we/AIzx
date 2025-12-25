<template>
  <view class="page">
    <view class="header">
      <view>
        <text class="location">上海</text>
        <text class="updated">更新于 09:30</text>
      </view>
      <text class="temp">26°</text>
    </view>

    <view class="card weather-card">
      <text class="condition">多云</text>
      <view class="meta">
        <text>湿度 60%</text>
        <text>风力 2级</text>
      </view>
    </view>

    <view class="card">
      <text class="section-title">空气质量</text>
      <view class="meta">
        <text>空气指数 58（良）</text>
      </view>
    </view>

    <view class="card">
      <text class="section-title">出行建议</text>
      <view class="tips">
        <text>携带雨具，短时有阵雨。</text>
        <text>晚间稍凉，注意添衣。</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {}
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
