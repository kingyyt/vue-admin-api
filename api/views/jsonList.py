from api import models
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

class jsonListSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.JsonInfo
        fields = "__all__"

class jsonListView(ListCreateAPIView):
    queryset = models.JsonInfo.objects.all()
    serializer_class=jsonListSerializers

class jsonDetailView(RetrieveUpdateDestroyAPIView):
    queryset = models.JsonInfo.objects.all()
    serializer_class=jsonListSerializers

