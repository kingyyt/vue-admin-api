from api import models
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.utils.jwt_auth import create_token


class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ['username','password']
        extra_kwargs = {'password': {'write_only': True}}

class RegisterView(GenericAPIView):
    """用户注册"""
    queryset = models.UserInfo.objects.all()
    serializer_class=RegisterSerializers
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        # 检查是否已存在用户
        exists = models.UserInfo.objects.filter(username=request.data.get('username')).exists() 
        if exists:
            return Response({"code":1002,"error":"用户已存在"})
        if serializer.is_valid():
            serializer.save()
            return Response({"code":1000,"success":"注册成功"})
        return Response({"code":1001,"error":serializer.errors})

class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ['username','password']

class LoginView(GenericAPIView):
    authentication_classes = []
    """用户登录"""
    queryset = models.UserInfo.objects.all()
    serializer_class=LoginSerializers
    #用户登录校验
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"code":1003,"error":"校验失败","detail":serializer.errors})
        instance = models.UserInfo.objects.filter(**serializer.validated_data).first()
        if not instance:
            return Response({"code":1002,"error":"用户名或密码错误"})
        token = create_token({"username":instance.username,"user_id":instance.id},60*60*24)

        instance.token = token
        instance.save()
        return Response({"code":1000,"token":token})
        
        


        