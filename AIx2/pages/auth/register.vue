<template>
  <view class="page">
    <view class="header">
      <text class="title">创建账号</text>
      <text class="subtitle">注册后即可同步资讯与日程</text>
    </view>

    <view class="form">
      <input class="input" type="text" v-model="username" placeholder="账号" />
      <input class="input" type="password" v-model="password" placeholder="密码" />
      <input class="input" type="password" v-model="confirm" placeholder="确认密码" />
      <button class="primary" @click="handleRegister">注册</button>
    </view>

    <view class="footer">
      <text>已有账号？</text>
      <text class="link" @click="goLogin">返回登录</text>
    </view>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  data() {
    return {
      username: '',
      password: '',
      confirm: ''
    }
  },
  methods: {
    handleRegister() {
      if (!this.username || !this.password) {
        uni.showToast({ title: '请输入账号和密码', icon: 'none' })
        return
      }
      if (this.password !== this.confirm) {
        uni.showToast({ title: '两次密码不一致', icon: 'none' })
        return
      }
      request({
        url: '/api/auth/register',
        method: 'POST',
        data: { username: this.username, password: this.password }
      })
        .then(() => {
          uni.showToast({ title: '注册成功，请登录', icon: 'none' })
          uni.navigateBack({ delta: 1 })
        })
        .catch(() => {
          uni.showToast({ title: '注册失败，请更换账号', icon: 'none' })
        })
    },
    goLogin() {
      uni.navigateBack({ delta: 1 })
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
  margin-bottom: 32rpx;
}
.title {
  font-size: 40rpx;
  font-weight: 600;
  color: #1c1d1f;
}
.subtitle {
  display: block;
  margin-top: 8rpx;
  color: #7a7f87;
  font-size: 26rpx;
}
.form {
  background: #fff;
  border-radius: 16rpx;
  padding: 32rpx;
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
  margin-top: 8rpx;
}
.footer {
  margin-top: 24rpx;
  text-align: center;
  font-size: 26rpx;
  color: #7a7f87;
}
.link {
  margin-left: 8rpx;
  color: #1c1d1f;
}
</style>
