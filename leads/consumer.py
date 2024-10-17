# leads/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'alert_group',  # Add to group
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'alert_group',
            self.channel_name
        )
