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
      const res = await GetJsonListDetail(81);
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
