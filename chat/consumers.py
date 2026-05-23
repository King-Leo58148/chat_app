
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from . models import Messages, Room
from django.core.serializers.json import DjangoJSONEncoder

active_users = {}
class ChatConsumer(AsyncWebsocketConsumer):
   async def connect(self):
      self.room_name = self.scope['url_route']['kwargs']['room_name']
      self.username = self.scope['url_route']['kwargs']['username']
      try: 
         await Room.objects.aget(name=self.room_name)
      except Room.DoesNotExist:
         await self.accept()
         await self.send(text_data=json.dumps
                        ({"error":"Room does not exist"}))
         await self.close()
         return 
      await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
            )
      await self.accept()
      if self.room_name not in active_users:
         active_users[self.room_name] = []
      active_users[self.room_name].append(self.username)

      await self.channel_layer.group_send(self.room_name,{'type': 'chat_message',
                                                           'username':'system',
                                                           'content':f"{self.username} has joined the chat"
                                 })
      messages = await sync_to_async(list)(
         Messages.objects.filter(room__name=self.room_name).order_by('time_stamp').values('content','username','reaction','time_stamp'))
      await self.send(text_data=json.dumps(messages,cls=DjangoJSONEncoder))
      

   async def disconnect(self,close_code):
     await self.channel_layer.group_send(self.room_name,{'type':'chat_message',
                                   'username':'system',
                                 'content':f"{self.username} has left the chat"
                                 })

     await self.channel_layer.group_discard(
       self.room_name,
       self.channel_name
     )
     if self.room_name in active_users:
         active_users[self.room_name].remove(self.username)
     
      

   async def receive(self,text_data):
     data = json.loads(text_data)
     
     room = await Room.objects.aget(name=self.room_name)
     await Messages.objects.acreate(content=data['content'],
                                    username = self.username,
                                    reaction = data.get('reaction',None),
                                    room = room
                                    )

     await self.channel_layer.group_send(self.room_name,{'type': 'chat_message', 
                                                           'username':self.username,
                                                           'content':data['content'],
                                    'reaction':data.get('reaction',None),
                                 }) 
     
   async def chat_message(self,event):
     event = json.dumps(event)
     await self.send(text_data=event)
   
     
    






    
