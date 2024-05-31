from api import models
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

class DemoView(GenericAPIView):

    def get(self,request):
        print(request.user)
        return Response("demo")
        