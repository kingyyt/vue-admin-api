<script lang="js">
import { tabbarToPage } from "@/utils/toPage"
export default {
  props: {
    props: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      active: 0,
      tabbars:null,
    };
  },
  mounted(){
      this.active = this.props.active

  },
  methods: {
    onChange(e) {
      uni.redirectTo({url:tabbarToPage(this.props.tabbars[e.detail].name)})
      uni.getStorage({
        key: "storage_tabbars",
        success: (res) => {
          this.tabbars = res.data;
          this.tabbars.tabbars.active = e.detail;
          uni.setStorage({
            key: "storage_tabbars",
            data: this.tabbars,
          });
        },
      });
    },
  },
};
</script>

<template>
  <div>
    <van-tabbar :active="active" @change="onChange">
      <van-tabbar-item
        v-for="(item, index) in props.tabbars"
        :key="index"
        :icon="item.icon"
      >
        {{ item.name }}
      </van-tabbar-item>
    </van-tabbar>
  </div>
</template>
