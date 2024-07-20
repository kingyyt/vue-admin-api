template = """
<template>
  <view v-if="tabbars" class="content">
    {{ template }}
  </view>
</template>
"""
script = """
<script>
{{ import }}

export default {
  components: {
    {{ components }}
  },
  data() {
    return {
      {{ data }}
    };
  },
  async onLoad() {
    {{ onLoad }}
  },
  methods: {
    {{ methods }}
  },
};


</script>
"""

utilsToPage = """
export const tabbarToPage = (page) => {
  switch (page) {
    case "首页":
      return "/pages/index/index";
    default:
      return "/pages/index/index";
  }
};

 """

pagesJson = {
  "globalStyle": {
    "navigationBarTextStyle": "black",
    "navigationBarTitleText": "uni-app",
    "navigationBarBackgroundColor": "#F8F8F8",
    "backgroundColor": "#F8F8F8",
    "usingComponents": {
      "van-button": "/wxcomponents/vant-weapp/button/index",
      "van-tabbar": "/wxcomponents/vant-weapp/tabbar/index",
      "van-tabbar-item": "/wxcomponents/vant-weapp/tabbar-item/index"
    }
  }
}

appVue = """
<script>
import { GetJsonListDetail } from "@/api/index";
export default {
  onLaunch: function () {
    this.init();
    this.getData();
  },
  methods: {
    init() {
      uni.removeStorage({
        key: "storage_data",
      });
    },
    async getData() {
      const res = await GetJsonListDetail({{ id }});
      console.log(res.data);
      uni.setStorage({
        key: "storage_data",
        data: res.data,
      });
      this.$isResolve();
    },
  },
};
</script>

<style>
/*每个页面公共css */
@import "@/wxcomponents/vant-weapp/common/index.wxss";

.van-tabbar {
  position: fixed;
  bottom: 0;
}
</style>
"""

toPage = """
export const tabbarToPage = (page) => {
  switch (page) {
    {{ toPage }}
    default:
      return "/pages/index/tabbar0";
  }
};
"""

onLoad = """
    await this.$onLaunched;
    this.getTabbarsValue();
"""

methods = """
    getTabbarsValue() {
      uni.getStorage({
        key: "storage_data",
        success: (res) => {
          this.tabbars = res.data.tabbars;
        },
      });
    },
"""
methodsNoTabbar = """
    getTabbarsValue() {
      uni.getStorage({
        key: "storage_data",
        success: (res) => {
          this.tabbars = res.data.json;
        },
      });
    },
"""