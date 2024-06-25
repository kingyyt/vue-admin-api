from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
import json

class BuildUniappFileConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect")
        await self.accept()
        await self.channel_layer.group_add('build_uniapp_file', self.channel_name)



    async def disconnect(self, close_code):

        await self.channel_layer.group_discard('build_uniapp_file', self.channel_name)

        raise StopConsumer()

    async def receive(self, text_data):
        # 这里可以处理接收到的WebSocket消息，例如开始构建过程
        await self.send(text_data=json.dumps({
            'message': 'Build started'
        }))

    async def send_progress(self, progress):
        if(progress.get('type')=='send_progress'):
            await self.send(text_data=json.dumps({
                'progress': progress.get('progress')
            }))
            return
        # 这个函数可以由其他进程或线程调用，以发送进度更新
        await self.send(text_data=json.dumps({
            'progress': progress
        }))