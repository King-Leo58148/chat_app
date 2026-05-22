import json
from sqlite3.dbapi2 import Timestamp
from channels.generic.websocket import AsyncWebsocketConsumer
from . models import Messages, Room
class ChatConsumer(AsyncWebsocketConsumer):
   async def connect(self):
    await self.accept()

   
   async def disconnect(self, close_code):
       pass
    
   async def receive(self,text_data):
     data = json.loads(text_data)
     
     room, _ = await Room.objects.aget_or_create(name=data['room'])
     await Messages.objects.acreate(content=data['content'],
                                    username = data['username'],
                                    reaction = data.get('reaction',None),
                                    room = room
                                    )

     await self.send(text_data = json.dumps(data))



    






    
