<template>
  <view class="page">
    <view class="header">
      <text class="title">账号信息</text>
      <text class="subtitle">管理你的基本资料</text>
    </view>
    <view class="card">
      <text class="label">昵称</text>
      <input class="input" v-model="form.username" placeholder="请输入昵称" />
      <text class="label">地区</text>
      <input class="input" v-model="form.location" placeholder="请输入地区" />
      <text class="label">邮箱（可选）</text>
      <input class="input" v-model="form.email" placeholder="请输入邮箱" />
      <text class="label">手机号（可选）</text>
      <input class="input" v-model="form.phone" placeholder="请输入手机号" />
      <text class="label">头像链接（可选）</text>
      <input class="input" v-model="form.avatar_url" placeholder="请输入头像链接" />
      <button class="primary" @click="saveProfile">保存资料</button>
    </view>

    <view class="card">
      <text class="label">修改密码</text>
      <input class="input" v-model="password.old_password" type="password" placeholder="旧密码" />
      <input class="input" v-model="password.new_password" type="password" placeholder="新密码" />
      <button class="ghost" @click="savePassword">更新密码</button>
    </view>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  data() {
    return {
      form: {
        username: '',
        location: '',
        email: '',
        phone: '',
        avatar_url: ''
      },
      password: {
        old_password: '',
        new_password: ''
      }
    }
  },
  onShow() {
    this.loadProfile()
  },
  methods: {
    loadProfile() {
      request({ url: '/api/user/profile' })
        .then((res) => {
          this.form = {
            username: res.username || '',
            location: res.location || '',
            email: res.email || '',
            phone: res.phone || '',
            avatar_url: res.avatar_url || ''
          }
        })
        .catch(() => {
          uni.showToast({ title: '加载资料失败', icon: 'none' })
        })
    },
    saveProfile() {
      request({ url: '/api/user/profile', method: 'PUT', data: this.form })
        .then(() => {
          uni.showToast({ title: '资料已更新', icon: 'none' })
        })
        .catch(() => {
          uni.showToast({ title: '保存失败', icon: 'none' })
        })
    },
    savePassword() {
      if (!this.password.old_password || !this.password.new_password) {
        uni.showToast({ title: '请填写旧密码和新密码', icon: 'none' })
        return
      }
      request({ url: '/api/user/password', method: 'PUT', data: this.password })
        .then(() => {
          this.password.old_password = ''
          this.password.new_password = ''
          uni.showToast({ title: '密码已更新', icon: 'none' })
        })
        .catch(() => {
          uni.showToast({ title: '密码更新失败', icon: 'none' })
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
  margin-bottom: 20rpx;
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.04);
}
.label {
  display: block;
  margin-top: 16rpx;
  font-size: 24rpx;
  color: #4b4f56;
}
.input {
  width: 100%;
  padding: 16rpx;
  border-radius: 12rpx;
  border: 1rpx solid #e5e7eb;
  margin-top: 8rpx;
}
.primary {
  margin-top: 24rpx;
  background: #1c1d1f;
  color: #fff;
  border: none;
}
.ghost {
  margin-top: 24rpx;
  background: #f3f4f6;
  color: #1c1d1f;
  border: none;
}
</style>
