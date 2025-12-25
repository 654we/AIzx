<template>
  <view class="page">
    <view class="header">
      <text class="title">资讯</text>
      <text class="subtitle">关注你关心的内容</text>
    </view>
    <view class="card" v-for="item in items" :key="item.id">
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
  </view>
</template>

<script>
export default {
  data() {
    return {
      items: [
        {
          id: '1',
          title: '今日热点标题示例',
          summary: '这里是摘要内容，展示 2~3 行以内的简短说明。',
          source: '示例来源',
          published_at: '09:00'
        }
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
</style>
