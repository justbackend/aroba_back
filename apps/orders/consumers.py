import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DispatcherOrdersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('dispatcher_group', self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("dispatcher_group", self.channel_name)
        await self.close(close_code)

    async def send_dispatcher_orders(self, event):
        data = json.dumps(event['data'])
        await self.send(data)


class FillingOrdersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("filling_group", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("filling_group", self.channel_name)
        await self.close()

    async def send_filling_orders(self, event):
        data = json.dumps(event['data'])
        await self.send(data)


class StatusOrdersConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(f"status_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("status_group", self.channel_name)
        await self.close()

    async def send_status_orders(self, event):
        data = json.dumps(event['data'])
        await self.send(data)


