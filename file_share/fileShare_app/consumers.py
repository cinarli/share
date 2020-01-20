# import asyncio
import json
from django.contrib.auth import get_user_model
# from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Comment,MyFile
# from .models import Thread,ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        
        self.room_group_name=self.scope['url_route']['kwargs']['room_name']
     
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self,text_data):
        text_data_json=json.loads(text_data)
        message=text_data_json['message']
        user=self.scope['user']
        new_message = await self.create_comment(user,message,self.room_group_name)

        await self.channel_layer.group_send(
            self.room_group_name,{
                'type':'chat_message',
                'message':new_message.reply,
                'user':new_message.User.username,
                'id':new_message.id
            }
        )

    async def chat_message(self,event):
        message=event['message']
        user = event['user']
        cid=event['id']
        await self.send(text_data=json.dumps({
            'message':message,
            'user': user,
            'comid':cid
        }))

    @database_sync_to_async
    def create_comment(self,user,comment,file):
        user=self.scope['user']
        obj=MyFile.objects.get(id=file)
        if obj.publish_comment or user==obj.user:
            message = Comment.objects.create(User=user,reply=comment,file_obj=obj)
            return message
        