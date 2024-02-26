import json

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from user_app.models import User

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()
#         print('Подключение установлено')

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         self.send(text_data=json.dumps({"message": message}))

# channel_layer = get_channel_layer()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        print("#######", data_json)
        
        send_data= json.dumps(data_json)
        await self.send(text_data=send_data)




# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # self.conf_name = self.scope['url_route']['kwargs']['conf_name']
#         # self.conf_group_name = f'conf_{self.conf_name}'

#         # await self.channel_layer.group_add(
#         #     self.conf_group_name,
#         #     self.channel_name
#         # )

#         # await channel_layer.send(self.channel_name, {
#         #     "type": "send.sdp",
#         #     "data": {'channel': self.channel_name},
#         # })
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.conf_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data_json = json.loads(text_data)
#         print("#######", data_json)
#         # message = data_json.get('message')
#         # action = data_json.get('action')
#         #
#         # if action == 'call':
#         #     channel_name, res_data = await self.call(message)
#         #     await channel_layer.send(channel_name, res_data)
#         #     return

#         data_json['channel'] = self.channel_name
#         await self.channel_layer.group_send(
#             self.conf_group_name,
#             {
#                 'type': 'send.sdp',
#                 'data': data_json,
#             }
#         )

#     async def send_sdp(self, event):
#         receive = event['data']
#         await self.send(text_data=json.dumps(receive))

#     async def call_message(self, event):
#         await self.send(text_data=json.dumps(event))

#     async def call(self, data):
#         try:
#             callee = await sync_to_async(User.objects.get)(login=data['login'])
#         except User.DoesNotExist:
#             return 'None', {"type": "chat.message", 'message': 'User does not connected!'}

#         return callee.channel_name, {
#             "type": "chat.message",
#             'calling': 'ok',
#             'callee': callee.login,
#             'room': self.conf_name
#         }