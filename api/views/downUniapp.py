from rest_framework import generics
from rest_framework.response import Response
from api import models
from rest_framework import serializers
import json
from api.ext.buildUniapp import read_and_build_file

class DownSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.BuildUniappFile
        fields = "__all__"

class downUniappView(generics.ListCreateAPIView):
    queryset = models.BuildUniappFile.objects.all()
    serializer_class = DownSerializers
    def get(self, request, *args, **kwargs):
        # 获取请求体中的 JSON 数据
        json_data = request.GET.get('json')
        try:
            # 将 JSON 字符串转换为 Python 对象（列表）
            data_list = json.loads(json_data)
            print(data_list)
            # 将data_list按需求引入相应代码
            id = read_and_build_file(data_list)
            print(id,'ididid')

        except json.JSONDecodeError:
            # 如果 JSON 解析失败，返回错误响应
            return Response({"error": "Invalid JSON data"}, status=400)

        # # 在这里，你可以使用 data_list 中的数据
        # # 例如，你可以直接使用这些数据，或者根据这些数据过滤查询集
        # filtered_queryset = self.queryset.filter(...)  # 使用 data_list 来构建过滤条件

        # # 使用 ListModelMixin 的 list 方法来序列化并返回结果
        # page = self.paginate_queryset(filtered_queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(filtered_queryset, many=True)
        return self.list(request)