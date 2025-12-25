<template>
  <view class="page">
    <view class="profile">
      <view class="avatar"></view>
      <view>
        <text class="name">未登录</text>
        <text class="desc">登录后管理你的偏好</text>
      </view>
    </view>

    <view class="card">
      <view class="row">
        <text>账号信息</text>
        <text class="arrow">›</text>
      </view>
      <view class="row">
        <text>订阅标签</text>
        <text class="arrow">›</text>
      </view>
      <view class="row">
        <text>位置设置</text>
        <text class="arrow">›</text>
      </view>
    </view>

    <button class="logout" type="default">退出登录</button>
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
.profile {
  display: flex;
  align-items: center;
  margin-bottom: 24rpx;
}
.avatar {
  width: 96rpx;
  height: 96rpx;
  border-radius: 50%;
  background: #dbe3f1;
  margin-right: 20rpx;
}
.name {
  font-size: 32rpx;
  font-weight: 600;
  color: #1c1d1f;
}
.desc {
  display: block;
  margin-top: 6rpx;
  color: #7a7f87;
  font-size: 24rpx;
}
.card {
  background: #fff;
  border-radius: 16rpx;
  padding: 12rpx 24rpx;
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.04);
}
.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1rpx solid #eef0f3;
  font-size: 28rpx;
}
.row:last-child {
  border-bottom: none;
}
.arrow {
  color: #c0c4cc;
}
.logout {
  margin-top: 32rpx;
  background: #fef2f2;
  color: #d92d20;
  border: none;
}
</style>
