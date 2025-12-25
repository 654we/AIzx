<template>
  <view class="page">
    <view class="header">
      <text class="title">日程</text>
      <text class="subtitle">本周安排一览</text>
    </view>

    <view class="actions">
      <button class="primary" @click="pickFile">上传日程文件</button>
      <button class="ghost" @click="loadLatest">获取最新日程</button>
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

    <view class="tips" v-if="tips.length">
      <text class="section-title">今日提示</text>
      <text v-for="(tip, index) in tips" :key="index">{{ tip }}</text>
    </view>
  </view>
</template>

<script>
import { request } from '../../utils/request'

export default {
  data() {
    return {
      times: ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00'],
      blocks: [],
      tips: []
    }
  },
  onShow() {
    this.loadLatest()
  },
  methods: {
    pickFile() {
      uni.chooseMessageFile({
        count: 1,
        type: 'file',
        extension: ['txt', 'md', 'csv'],
        success: (res) => {
          const file = res.tempFiles[0]
          if (!file) return
          uni.uploadFile({
            url: 'http://localhost:8000/api/schedule/upload',
            filePath: file.path,
            name: 'file',
            header: {
              Authorization: `Bearer ${uni.getStorageSync('token')}`
            },
            success: (uploadRes) => {
              const data = JSON.parse(uploadRes.data)
              this.applyPlan(data)
              uni.showToast({ title: '上传成功', icon: 'none' })
            },
            fail: () => {
              uni.showToast({ title: '上传失败', icon: 'none' })
            }
          })
        }
      })
    },
    loadLatest() {
      request({ url: '/api/schedule/latest' })
        .then((res) => {
          this.applyPlan(res)
        })
        .catch(() => {
          this.blocks = []
          this.tips = ['暂无日程，请先上传文件']
        })
    },
    applyPlan(plan) {
      const blocks = []
      plan.week.forEach((day) => {
        day.blocks.forEach((block, index) => {
          blocks.push({
            id: `${day.date}-${index}`,
            title: block.title,
            time: `${block.start}-${block.end}`,
            location: block.location
          })
        })
      })
      this.blocks = blocks
      this.tips = plan.tips || []
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
.actions {
  display: flex;
  gap: 16rpx;
  margin-bottom: 24rpx;
}
.primary {
  flex: 1;
  background: #1c1d1f;
  color: #fff;
  border: none;
}
.ghost {
  flex: 1;
  background: #fff;
  color: #1c1d1f;
  border: 1rpx solid #e5e7eb;
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
.tips {
  margin-top: 24rpx;
  background: #fff;
  border-radius: 16rpx;
  padding: 20rpx 24rpx;
  box-shadow: 0 8rpx 20rpx rgba(0, 0, 0, 0.04);
}
.tips text {
  display: block;
  margin-top: 12rpx;
  font-size: 24rpx;
  color: #4b4f56;
}
.section-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #1c1d1f;
}
</style>
