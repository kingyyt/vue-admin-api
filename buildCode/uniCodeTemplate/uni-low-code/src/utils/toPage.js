export const tabbarToPage = (page) => {
  switch (page) {
    case "首页":
      return "/pages/index/index";
    case "分类页":
      return "/pages/index/tabbar1";
    case "购物车":
      return "/pages/index/tabbar2";
    case "我的":
      return "/pages/index/tabbar3";
    default:
      return "/pages/index/index";
  }
};
