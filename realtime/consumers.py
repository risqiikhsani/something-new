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

from .serializers import *


class NotificationConsumer(WebsocketConsumer):
    def connect(self):

        user = self.scope["user"]

        self.room_group_name = "notification_%s" % user.id
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        # Client.objects.create(user=user,channel_name=self.channel_name,server="app_notification")

        print("connected = "+self.channel_name)

        a, created = ClientSocketData.objects.get_or_create(
            user=user,
            server_name=self.room_group_name
        )
        a.save()

        self.accept()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'app_notification',
                "data": None,
            }
        )

    def disconnect(self, close_code):
        # Client.objects.filter(channel_name=self.channel_name).delete()

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # def notifications_are_read(self, data):
    #     print("notifications_are_read function is running")

    def receive(self, text_data):
        print("data is received")
        text_data_json = json.loads(text_data)
        data = text_data_json["data"]
        command = text_data_json["command"]

        match command:
            case "notifications_are_read":
                # self.notifications_are_read(self, data)
                user = self.scope["user"]
                last_read_notification_id = Notification.objects.filter(user=user).latest('id').id
                a = ClientSocketData.objects.get(
                    user=user,
                    server_name=self.room_group_name
                )
                a.last_read_id_in_server = last_read_notification_id
                a.save()

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'app_notification',
                        "data": None,
                    }
                )
            case _:
                pass

        # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name, {
        #         "type": "chat_message",
        #         "message": message,
        #         "sender": sender,
        #     }
        # )

    def app_notification(self, event):
        print("send_notification event is running")
        print(event["data"])

        user = self.scope["user"]
        a = ClientSocketData.objects.get(
            user=user,
            server_name=self.room_group_name
        )
        b = a.last_read_id_in_server

        c = user.notification_set.all().filter(id__gt=b).count()

        self.send(text_data=json.dumps({
            "type": "app_notification",
            "data": event["data"],
            "unread_items": c
        }))

    def chat_notification(self, event):
        print("send_notification event is running")
        self.send(text_data=json.dumps({
            "type": "chat_notification",
            "data": event["data"],
        }))


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(self.channel_name + " is connected")
        self.room_name = self.scope["url_route"]["kwargs"]["room_id"]
        user = self.scope["user"]

        a = ChatRoom.objects.get(id=self.room_name)
        if user not in a.user.all():
            self.close()
        
        self.room_group_name = "chatroom_%s" % self.room_name

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

        data = text_data_json["data"]
        command = text_data_json["command"]

        match command:
            case "chat":

                user = self.scope["user"]
                a = ChatRoom.objects.get(id=self.room_name)
                b = Chat.objects.create(
                    sender=user,
                    text=data["text"],
                )

                b.room.add(a)

                if "reply_from" in data:
                    z = Chat.objects.get(id=data["reply_from"])
                    b.reply_from = z

                b.save()

                # Send message to room group
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name, {
                        "type": "chat_message",
                        "data": Chat_Serializer(instance=b).data
                    }
                )
            case _:
                pass

        

    # Receive message from room group
    def chat_message(self, event):

        data = event["data"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "data": data,
            "type": "chat_message_ws",
        }))

    def chat_notification(self, event):

        data = event["data"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "data": data,
            "type": "chat_notification_ws",
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
