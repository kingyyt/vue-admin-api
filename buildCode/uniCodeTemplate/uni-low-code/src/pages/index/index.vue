<template>
  <view class="content">
    <image class="logo" src="/static/logo.png"></image>
    <view>
      <text class="title">{{ title }}</text>
      <van-button>123</van-button>
    </view>
  </view>
</template>

<script>
import { GetJsonListDetail } from "@/api/index";
export default {
  data() {
    return {
      title: "Hello",
    };
  },
  onLoad() {
    this.init();
  },
  methods: {
    async init() {
      const res = await GetJsonListDetail(1);
      console.log(res);
    },
  },
};
</script>

<style>
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.logo {
  height: 200rpx;
  width: 200rpx;
  margin: 200rpx auto 50rpx auto;
}

.text-area {
  display: flex;
  justify-content: center;
}

.title {
  font-size: 36rpx;
  color: #8f8f94;
}
</style>
