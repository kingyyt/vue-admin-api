<template>
  <view class="content">
    <van-button type="danger"></van-button>
    <view v-for="(item, index) in dynamicComponent" :key="index">
      <!-- <component :is="item.comName" :props="item.props"></component> -->
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { allLoadComponent } from "@/utils/getPackages/getComponent";
import { GetJsonListDetail } from "@/api/microMain/microMain";
import type { JsonListData } from "@/api/microMain/model/microModel";

let list = ref([]);

let dynamicComponent = ref<any[]>([]);
const getJsonList = async () => {
  const res = (await GetJsonListDetail(1)) as JsonListData | null;
  if (res) {
    console.log(res);
    list.value = JSON.parse(res.json);
    // webview方案
    dynamicComponent.value = await allLoadComponent(list.value);
    console.log(dynamicComponent.value);
  }
};
onMounted(() => {
  getJsonList();
});
</script>

<style></style>
