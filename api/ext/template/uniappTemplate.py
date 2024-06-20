template = """
<template>
  <view class="content">
    {{ template }}
  </view>
</template>
"""
script = """
<script setup lang="ts">
import { GetJsonListDetail } from '@/api/microMain/microMain'
import type { JsonListData } from '@/api/microMain/model/microModel'
{{ import }}

{{ data }}
</script>
"""