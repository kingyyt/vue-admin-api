from rest_framework.response import Response
import jwt
from django.conf import settings
from jwt import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JwtAuthView(BaseAuthentication):
    def authenticate(self, request):
        # 如果是接口文档请求，直接返回一个空的身份验证对象
        if request.path == '/swagger/' or request.path == '/redoc/':
            return (None, None)
        token = request.query_params.get('token') or request.META.get('HTTP_AUTHORIZATION', '')
        payload = None
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
        except exceptions.ExpiredSignatureError:
            raise AuthenticationFailed({'code':1003,'error':'token 已过期'})
        except jwt.DecodeError:
            raise AuthenticationFailed({'code':1003,'error':'token 认证失败'})
        except jwt.InvalidTokenError:
            raise AuthenticationFailed({'code':1003,'error':'token 非法'})
        # print(payload['user_id'],payload['username'])
        return (payload,token)