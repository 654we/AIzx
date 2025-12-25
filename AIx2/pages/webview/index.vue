<template>
  <view class="page">
    <web-view :src="url"></web-view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      url: ''
    }
  },
  onLoad(options) {
    this.url = decodeURIComponent(options.url || '')
  }
}
</script>

<style scoped>
.page {
  min-height: 100vh;
}
</style>
