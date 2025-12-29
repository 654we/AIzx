<template>
  <view class="page">
    <view class="header">
      <text class="title">订阅标签</text>
      <text class="subtitle">管理你的资讯偏好</text>
    </view>
    <view class="card">
      <view class="row">
        <input class="input" v-model="newTag" placeholder="输入标签" />
        <button class="primary" @click="addTag">添加</button>
      </view>
      <view class="tags">
        <view v-for="(tag, index) in tags" :key="index" class="tag">
          <text>{{ tag }}</text>
          <text class="remove" @click="removeTag(index)">×</text>
        </view>
      </view>
      <button class="ghost" @click="saveTags">保存标签</button>
    </view>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  data() {
    return {
      tags: [],
      newTag: ''
    }
  },
  onShow() {
    this.loadTags()
  },
  methods: {
    loadTags() {
      request({ url: '/api/user/subscriptions' })
        .then((res) => {
          this.tags = res.tags || []
        })
        .catch(() => {
          uni.showToast({ title: '获取标签失败', icon: 'none' })
        })
    },
    addTag() {
      const tag = this.newTag.trim()
      if (!tag) return
      if (this.tags.includes(tag)) {
        uni.showToast({ title: '标签已存在', icon: 'none' })
        return
      }
      this.tags.push(tag)
      this.newTag = ''
    },
    removeTag(index) {
      this.tags.splice(index, 1)
    },
    saveTags() {
      request({ url: '/api/user/subscriptions', method: 'PUT', data: { tags: this.tags } })
        .then(() => {
          uni.showToast({ title: '标签已保存', icon: 'none' })
        })
        .catch(() => {
          uni.showToast({ title: '保存失败', icon: 'none' })
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
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.04);
}
.row {
  display: flex;
  gap: 16rpx;
}
.input {
  flex: 1;
  padding: 16rpx;
  border-radius: 12rpx;
  border: 1rpx solid #e5e7eb;
}
.primary {
  background: #1c1d1f;
  color: #fff;
  border: none;
}
.tags {
  margin-top: 16rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}
.tag {
  background: #f3f4f6;
  border-radius: 12rpx;
  padding: 8rpx 16rpx;
  display: flex;
  align-items: center;
  gap: 8rpx;
  font-size: 24rpx;
}
.remove {
  color: #d92d20;
}
.ghost {
  margin-top: 20rpx;
  background: #f3f4f6;
  color: #1c1d1f;
  border: none;
}
</style>
