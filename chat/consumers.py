import json
from channels.generic.websocket import AsyncWebsocketConsumer
from . models import Messages, Room
class ChatConsumer(AsyncWebsocketConsumer):
   async def connect(self):
      self.room_name = self.scope['url_route']['kwargs']['room_name']
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

   async def disconnect(self,close_code):
     await self.channel_layer.group_discard(
       self.room_name,
       self.channel_name
     )
      

   async def receive(self,text_data):
     data = json.loads(text_data)
     
     room = await Room.objects.aget(name=self.room_name)
     await Messages.objects.acreate(content=data['content'],
                                    username = data['username'],
                                    reaction = data.get('reaction',None),
                                    room = room
                                    )

     await self.channel_layer.group_send(self.room_name,{'type': 'chat_message', 
                                                           'username':data['username'],
                                                           'content':data['content'],
                                    'reaction':data.get('reaction',None),
                                 }) 
     
   async def chat_message(self,event):
     event = json.dumps(event)
     await self.send(text_data=event)
     
    






    
