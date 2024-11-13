from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/dispatcher-orders', consumers.DispatcherOrdersConsumer.as_asgi()),
    re_path(r'ws/status-orders', consumers.StatusOrdersConsumer.as_asgi()),
    re_path(r'ws/filling-orders', consumers.FillingOrdersConsumer.as_asgi()),
]
