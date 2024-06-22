from rest_framework import generics
from rest_framework.response import Response
from api import models
from rest_framework import serializers
import json
from api.ext.buildUniapp import read_and_build_file
from api.ext.auth import JwtAuthView

class DownSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.BuildUniappFile
        fields = "__all__"

class downUniappView(generics.ListCreateAPIView):
    queryset = models.BuildUniappFile.objects.all()
    authentication_classes = [JwtAuthView]
    serializer_class = DownSerializers
    
    def get_queryset(self):
        payload, token = self.request.successful_authenticator.authenticate(self.request)
        user = payload['user_id']
        return user
    def post(self, request, *args, **kwargs):
        user_info = models.UserInfo.objects.get(id=self.get_queryset()) 
        json_data = request.data["json"]
        # 获取请求体中的 JSON 数据
        try:
            # 将 JSON 字符串转换为 Python 对象（列表）
            data_list = json.loads(json_data)
            print(data_list)
            # 将data_list按需求引入相应代码
            id = read_and_build_file(data_list)

        except json.JSONDecodeError:
            # 如果 JSON 解析失败，返回错误响应
            return Response({"error": "Invalid JSON data"}, status=400)

        print(id,'ididid')
        instance = models.BuildUniappFile.objects.create(user_id=user_info,filename=id)
        instance.save()

    # def get(self, request, *args, **kwargs):
    #     # 获取请求体中的 JSON 数据
    #     json_data = request.GET.get('json')
    #     try:
    #         # 将 JSON 字符串转换为 Python 对象（列表）
    #         data_list = json.loads(json_data)
    #         print(data_list)
    #         # 将data_list按需求引入相应代码
    #         id = read_and_build_file(data_list)

    #     except json.JSONDecodeError:
    #         # 如果 JSON 解析失败，返回错误响应
    #         return Response({"error": "Invalid JSON data"}, status=400)

    #     print(id,'ididid')
        
        return Response({'code': 1000, 'msg': '打包成功', 'name': {"id":id}})