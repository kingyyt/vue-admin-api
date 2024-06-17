import Http from '@/http/httpRequest'

enum Api {
  UNI_JSONLISTDETAIL = '/api/uni/jsonListDetail/'
}
export const GetJsonListDetail = (id: number) => Http.getRequest(`${Api.UNI_JSONLISTDETAIL}${id}/`)
