<template>
  <view class="content"> </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { GetJsonListDetail } from '@/api/microMain/microMain'
import type { JsonListData } from '@/api/microMain/model/microModel'

let list = ref([])

// let dynamicComponent = ref<any[]>([]);
const getJsonList = async () => {
  const res = (await GetJsonListDetail(1)) as JsonListData | null
  if (res) {
    console.log(res)
    list.value = JSON.parse(res.json)
  }
}
onMounted(() => {
  getJsonList()
})
</script>

<style></style>
