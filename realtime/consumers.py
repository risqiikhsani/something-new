# import json

# from channels.generic.websocket import WebsocketConsumer


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         self.send(text_data=json.dumps({"message": message}))


####################################################################################################

import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .models import *


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        # self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name, self.channel_name
        # )

        user = self.scope["user"]

        self.room_group_name = "notification_%s" % user.id

        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        Client.objects.create(user=user,channel_name=self.channel_name,server="app_notification")

        print("connected = "+self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        # # Leave room group
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name, self.channel_name
        # )
        Client.objects.filter(channel_name=self.channel_name).delete()
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # def receive(self, text_data):
    #     print('receive')
    #     text_data_json = json.loads(text_data)
    #     text = text_data_json["text"]
    #     # Send message to room group
    #     async_to_sync(self.channel_layer.send)(
    #         self.channel_name, {
    #             "type": "send_notification",
    #             "text": "helo",
    #         }
    #     )

    def send_notification(self, event):
        print("send_notification event is running")
        self.send(text_data=event["text"])


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(self.channel_name + " is connected")
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    # Menerima message dari websocket , kemudian kirim ke group channel layer
    def receive(self, text_data):
        print("received text_data = " + text_data+" in "+self.channel_name)
        text_data_json = json.loads(text_data)

        message = text_data_json["message"]
        sender = text_data_json["sender"]
        command = text_data_json["command"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "sender": sender,
            }
        )

    # Receive message from room group
    def chat_message(self, event):

        message = event["message"]
        sender = event["sender"]
        print("chat_message is running = "+message+" in "+self.channel_name)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "message": message,
            "type": "chat_text",
            "sender": sender,
        }))

####################################################################################################


# import json

# from channels.generic.websocket import AsyncWebsocketConsumer


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name

#         # Join room group
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     # Receive message from WebSocket
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]

#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name, {"type": "chat_message", "message": message}
#         )

#     # Receive message from room group
#     async def chat_message(self, event):
#         message = event["message"]

#         # Send message to WebSocket
#         await self.send(text_data=json.dumps({"message": message}))
