<template>
  <view class="page">
    <view class="profile">
      <view class="avatar"></view>
      <view>
        <text class="name">{{ username }}</text>
        <text class="desc">{{ description }}</text>
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

    <button v-if="!isLoggedIn" class="login" type="default" @click="goLogin">登录 / 注册</button>
    <button v-else class="logout" type="default" @click="handleLogout">退出登录</button>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  data() {
    return {
      isLoggedIn: false,
      username: '未登录',
      description: '登录后管理你的偏好'
    }
  },
  onShow() {
    this.refreshProfile()
  },
  methods: {
    refreshProfile() {
      const token = uni.getStorageSync('token')
      this.isLoggedIn = Boolean(token)
      if (!token) {
        this.username = '未登录'
        this.description = '登录后管理你的偏好'
        return
      }
      request({ url: '/api/user/profile' })
        .then((res) => {
          this.username = res.username || '已登录'
          this.description = '账号信息已同步'
        })
        .catch(() => {
          this.username = '已登录'
          this.description = '账号信息获取失败'
        })
    },
    goLogin() {
      uni.navigateTo({ url: '/pages/auth/login' })
    },
    handleLogout() {
      uni.removeStorageSync('token')
      this.isLoggedIn = false
      this.username = '未登录'
      this.description = '登录后管理你的偏好'
      uni.showToast({ title: '已退出登录', icon: 'none' })
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
.login {
  margin-top: 32rpx;
  background: #1c1d1f;
  color: #fff;
  border: none;
}
</style>
