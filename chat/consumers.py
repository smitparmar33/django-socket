#https://dev.to/earthcomfy/django-channels-a-simple-chat-app-part-2-eh9
#https://hirelofty.com/blog/software-development/django-channels/
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer,AsyncJsonWebsocketConsumer

class UserConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        await self.accept()
        await self.channel_layer.group_add(self.user_name, self.channel_name)

    async def disconnect(self, code):
        print('disconnected')
        await self.channel_layer.group_discard(self.user_name, self.channel_name)
        print(f'removed {self.channel_name}')

    async def websocket_receive(self, message):
        print(message)
        return super().websocket_receive(message)

    async def websocket_send(self, event):
        await self.send_json(event)

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        print(self.channel_layer,self.room_group_name)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
