from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .dispatchers.serializers import NewOrdersListSerializer, FillingOrdersListSerializer
from .serializers import FullOrderSerializer


def send_socket_data(channel, method, data, channel_layer=None):
    channel_layer = channel_layer or get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        channel,
        {
            "type": method,
            'data': data,
        }
    )


class SocketSendOrders:

    @classmethod
    def get_order_data(cls, order, action, serializer=None):
        serializer = serializer or FullOrderSerializer

        if action != 'd':
            return dict(action=action, data=serializer(order).data)
        return dict(action=action, data=dict(id=order.id))

    @classmethod
    def ws_filling_orders(cls, order, action='c'):

        send_socket_data(
            channel='filling_group',
            data=cls.get_order_data(order, action, serializer=FillingOrdersListSerializer),
            method='send_filling_orders'
        )

    @classmethod
    def ws_status_orders(cls, order, action='c'):
        send_socket_data(
            channel='status_group',
            data=cls.get_order_data(order, action),
            method='send_status_orders'
        )

    @classmethod
    def ws_dispatcher_orders(cls, order, action='c'):
        send_socket_data(
            channel='dispatcher_group',
            data=cls.get_order_data(order, action, serializer=NewOrdersListSerializer),
            method='send_dispatcher_orders',
        )
