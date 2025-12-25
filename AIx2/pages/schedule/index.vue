<template>
  <view class="page">
    <view class="header">
      <text class="title">日程</text>
      <text class="subtitle">本周安排一览</text>
    </view>

    <view class="table">
      <view class="time-column">
        <text v-for="time in times" :key="time" class="time">{{ time }}</text>
      </view>
      <view class="grid">
        <view v-for="item in blocks" :key="item.id" class="block">
          <text class="block-title">{{ item.title }}</text>
          <text class="block-meta">{{ item.time }} · {{ item.location }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      times: ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00'],
      blocks: [
        { id: 1, title: '英语课', time: '08:00-09:30', location: '线上' },
        { id: 2, title: '项目会议', time: '14:00-15:00', location: 'A201' }
      ]
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
.table {
  display: flex;
  background: #fff;
  border-radius: 16rpx;
  padding: 24rpx;
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.04);
}
.time-column {
  width: 120rpx;
  border-right: 1rpx solid #eef0f3;
}
.time {
  display: block;
  font-size: 22rpx;
  color: #7a7f87;
  padding: 12rpx 0;
}
.grid {
  flex: 1;
  padding-left: 24rpx;
}
.block {
  background: #f0f6ff;
  border-radius: 12rpx;
  padding: 16rpx;
  margin-bottom: 16rpx;
}
.block-title {
  font-size: 26rpx;
  font-weight: 600;
  color: #1c1d1f;
}
.block-meta {
  display: block;
  margin-top: 8rpx;
  font-size: 22rpx;
  color: #6b7280;
}
</style>
