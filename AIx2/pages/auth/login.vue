<template>
  <view class="page">
    <view class="header">
      <text class="title">欢迎回来</text>
      <text class="subtitle">登录后管理你的偏好</text>
    </view>

    <view class="form">
      <input class="input" type="text" v-model="username" placeholder="账号" />
      <input class="input" type="password" v-model="password" placeholder="密码" />
      <button class="primary" @click="handleLogin">登录</button>
      <button class="wechat" @click="handleWechatLogin">微信登录</button>
    </view>

    <view class="footer">
      <text>还没有账号？</text>
      <text class="link" @click="goRegister">立即注册</text>
    </view>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  data() {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    handleLogin() {
      if (!this.username || !this.password) {
        uni.showToast({ title: '请输入账号和密码', icon: 'none' })
        return
      }
      request({
        url: '/api/auth/login',
        method: 'POST',
        data: { username: this.username, password: this.password }
      })
        .then((res) => {
          uni.setStorageSync('token', res.access_token)
          uni.switchTab({ url: '/pages/mine/index' })
        })
        .catch(() => {
          uni.showToast({ title: '登录失败，请检查账号密码', icon: 'none' })
        })
    },
    handleWechatLogin() {
      uni.login({
        provider: 'weixin',
        success: (result) => {
          request({
            url: '/api/auth/wechat_login',
            method: 'POST',
            data: { code: result.code }
          })
            .then((res) => {
              uni.setStorageSync('token', res.access_token)
              uni.switchTab({ url: '/pages/mine/index' })
            })
            .catch(() => {
              uni.showToast({ title: '微信登录失败', icon: 'none' })
            })
        },
        fail: () => {
          uni.showToast({ title: '微信登录不可用', icon: 'none' })
        }
      })
    },
    goRegister() {
      uni.navigateTo({ url: '/pages/auth/register' })
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
.wechat {
  margin-top: 16rpx;
  background: #e7f8ef;
  color: #12b76a;
  border: none;
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
