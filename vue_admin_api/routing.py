from django.urls import path

from api import consumers

websocket_urlpatterns = [
    path('ws/build_uniapp_file/', consumers.BuildUniappFileConsumer.as_asgi()),
]