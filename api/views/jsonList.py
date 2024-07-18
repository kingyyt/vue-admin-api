from api import models
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from api.ext.auth import JwtAuthView
import json

class jsonListSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.JsonInfo
        fields = "__all__"

class jsonListView(ListCreateAPIView):
    authentication_classes = [JwtAuthView]
    serializer_class = jsonListSerializers
    def get_queryset(self):
        payload, token = self.request.successful_authenticator.authenticate(self.request)
        user = payload['user_id']
        return user
        
    def get(self, request, *args, **kwargs):
        queryset = models.JsonInfo.objects.filter(user_id=self.get_queryset())
        serializer = jsonListSerializers(queryset, many=True).data
        return Response({'code': 1000, 'msg': '获取成功', 'data': serializer})

    def post(self,request, *args, **kwargs):
        user_info = models.UserInfo.objects.get(id=self.get_queryset())  
        instance = models.JsonInfo.objects.create(user_id=user_info,**request.data)
        instance.save()
        serializer = jsonListSerializers(instance).data
        return Response({'code':1000,'msg' : '添加成功','data':serializer})


class jsonDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JwtAuthView]
    serializer_class=jsonListSerializers
    def get_queryset(self):
        payload,token = self.request.successful_authenticator.authenticate(self.request)
        user = payload['user_id']
        return models.JsonInfo.objects.filter(user_id=user)


class uniJsonDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    serializer_class=jsonListSerializers
    def get_queryset(self):
        id = self.kwargs['pk']
        data = models.JsonInfo.objects.filter(id=id)
        serializer = jsonListSerializers(data, many=True).data[0]
        serializer['json'] = json.loads(serializer.get('json'))
        tabbars = []
        # 判断tabbars是否存在
        if serializer.get('tabbars'):
            tabbars = json.loads(serializer.get('tabbars'))
            if tabbars.get('isUseTabbar'):
                # 获取tabbars的所有id
                id_list = []
                for item in range(len(tabbars.get('tabbars').get('tabbars'))):
                    id_list.append(tabbars.get('tabbars').get('tabbars')[item].get('select'))

                data_list = models.JsonInfo.objects.filter(id__in=id_list)
                serializer_data_list = jsonListSerializers(data_list, many=True).data
                # 根据tabbars 拼接页面数据
                for tabbar in tabbars.get('tabbars').get('tabbars'):
                    for select in serializer_data_list:
                            if tabbar.get('select') == select.get('id'):
                                # print(select['json'],'----')
                                tabbar['json'] = json.loads(select['json'])
                serializer['tabbars'] = tabbars
        
                
        return serializer
        
        
    def get(self, request, *args, **kwargs):
        return Response({'code': 1000, 'msg': '获取成功', 'data': self.get_queryset()})