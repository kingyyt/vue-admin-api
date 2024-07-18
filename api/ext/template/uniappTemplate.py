template = """
<template>
  <view class="content">
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
  onLoad() {},
  methods: {},
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

pagesJson = """
{
  "pages": [
    {
      "path": "pages/index/index",
      "style": {
        "navigationBarTitleText": "首页"
      }
    },
  ],

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

"""