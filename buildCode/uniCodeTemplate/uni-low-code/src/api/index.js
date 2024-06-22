import Http from "./http/httpRequest";
const Api = {
  UNI_JSONLISTDETAIL: "/api/uni/jsonListDetail/",
};
export const GetJsonListDetail = (id) =>
  Http.getRequest(`${Api.UNI_JSONLISTDETAIL}${id}/`);
