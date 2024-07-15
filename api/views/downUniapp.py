from rest_framework import generics
from rest_framework.response import Response
from api import models
from rest_framework import serializers
import json
from api.ext.buildUniapp import read_and_build_file
from api.ext.auth import JwtAuthView
import os
import zipfile
from django.http import FileResponse
from channels.layers import get_channel_layer

class jsonListSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.JsonInfo
        fields = "__all__"


class DownSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.BuildUniappFile
        fields = "__all__"

class downUniappZipView(generics.CreateAPIView):
    queryset = models.BuildUniappFile.objects.all()
    authentication_classes = [JwtAuthView]
    serializer_class = DownSerializers
    def get_queryset(self):
        payload, token = self.request.successful_authenticator.authenticate(self.request)
        user = payload['user_id']
        return user

    def post(self, request, *args, **kwargs):
        folder_name = request.query_params.get("filename")
        if not folder_name:
            return Response({"error": "传入的文件名错误"}, status=401)
        # 确保文件夹存在
        folder_path = os.path.join("buildCode", "DoneCode", folder_name)
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return Response({"error": "文件不存在"}, status=402)

        # 创建一个临时ZIP文件
        zip_file_name = f"{folder_name}.zip"
        zip_file_path = os.path.join("/tmp", zip_file_name)

        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))

        # 返回ZIP文件作为响应
        response = FileResponse(open(zip_file_path, 'rb'), content_type='application/zip',status=206)
        response['Content-Disposition'] = f'attachment; filename="{zip_file_name}"'
        return response

class downUniappView(generics.CreateAPIView):
    queryset = models.BuildUniappFile.objects.all()
    authentication_classes = [JwtAuthView]
    serializer_class = DownSerializers
    def get_queryset(self):
        payload, token = self.request.successful_authenticator.authenticate(self.request)
        user = payload['user_id']
        return user
    def post(self, request, *args, **kwargs):
        user_info = models.UserInfo.objects.get(id=self.get_queryset()) 
        # json_data = request.data["json"]
        id = request.data["id"]
        # 获取json数据
        json_info = models.JsonInfo.objects.filter(id=id) 
        # 获取请求体中的 JSON 数据
        json_info_serializer = jsonListSerializers(json_info, many=True).data
        json_data = json_info_serializer[0]["json"]
        # 判断tabbar是否存在
        if "tabbars" in json_info_serializer[0]:
            tabbars_data = json_info_serializer[0]["tabbars"]
            data_tabbar = json.loads(tabbars_data)
        else:
            tabbars_data = {}
        channel_layer = get_channel_layer()
        try:
            # 将 JSON 字符串转换为 Python 对象（列表）
            data_list = json.loads(json_data)
            # # 获取WebSocket的channel_layer
            # 将data_list按需求引入相应代码
            id = read_and_build_file(data_list,channel_layer,data_tabbar)

        except json.JSONDecodeError:
            # 如果 JSON 解析失败，返回错误响应
            return Response({"error": "Invalid JSON data"}, status=400)

        instance = models.BuildUniappFile.objects.create(user_id=user_info,filename=id)
        instance.save()

        return Response({'code': 1000, 'msg': '打包成功', 'name': {"id":id},'data_tabbar':data_tabbar},status=207)
