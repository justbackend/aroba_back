from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response

from utils import *
from utils.choices import *
from . import serializers
from .. import models
from ..utils import SocketSendOrders


class AdditionalAmountView(generics.UpdateAPIView):
    serializer_class = serializers.AdditionalAmountSerializer
    http_method_names = 'patch',

    def get_object(self):
        return get_object(
            models.Order,
            q_objects=~Q(payments__type=PaymentTypes.EXTRA),
            id=self.kwargs['order_id'],
        )


class StatusOrdersListView(generics.ListAPIView):
    serializer_class = serializers.StatusOrdersListSerializer
    filterset_fields = ('client', 'status', 'payment_type')
    search_fields = ('car_number', 'code', 'driver_phone')

    def get_queryset(self):
        user = self.request.user
        query = dict(dispatcher=user)

        if user.is_superuser:
            query = dict()

        return (
            models.Order.objects.filter(
                status__in=(OrderStatus.STARTED, OrderStatus.AT_FACTORY,
                            OrderStatus.LOADED, OrderStatus.LOCATION_ASSIGNED),
                **query
            ).select_related('loading', 'client', 'unloading').order_by('-id')
        )


class RollbackOrderView(generics.GenericAPIView):
    serializer_class = serializers.DeleteOrderStatusSerializer

    def patch(self, request, order_id, *args, **kwargs):
        order = get_object(models.Order, q_objects=~Q(status__in=(OrderStatus.NEW, OrderStatus.FILLING)), id=order_id)
        first_status = order.status
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.validated_data['comment']
        order.clear(
            fields=('car_number', 'income', 'driver_phone', 'total_amount', 'dispatcher')
        )
        order.status = OrderStatus.NEW
        order.paid = False
        order.save()
        order.payments.all().delete()

        log_com = (f"Buyurtma Qaytarildi!!! \n"
                   f"Comment: {comment}\n")
        order.create_log(
            action=OrderLogActions.ROLLBACK,
            user=request.user,
            comment=log_com,
        )
        SocketSendOrders.ws_dispatcher_orders(action='u', order=order)

        method_name = 'ws_filling_orders' if first_status == OrderStatus.FILLING else 'ws_status_orders'
        getattr(SocketSendOrders, method_name)(order, 'd')

        return Response({'msg': "Success"})


class UpdateOrderStatusView(generics.UpdateAPIView):
    serializer_class = serializers.UpdateOrderStatusSerializer
    http_method_names = 'patch',
    log_comment = "Buyurtma statusi Yangiladi\n\nEski: {} -> Yangi: {}"
    statuses = dict(OrderStatus.choices)

    def get_object(self):
        return get_object(
            models.Order, id=self.kwargs['pk'],
            status__gte=OrderStatus.STARTED,
            income__isnull=False,
            total_amount__isnull=False,
        )

    def perform_update(self, serializer):
        old_status = self.statuses[serializer.instance.status]
        serializer.save()
        instance = serializer.instance
        new_status = self.statuses[instance.status]
        if old_status != new_status:
            comment = self.log_comment.format(old_status, new_status)
            instance.create_log(user=self.request.user, comment=comment, action=OrderLogActions.UPDATE)

        SocketSendOrders.ws_status_orders(action='u', order=instance)


class DeleteOrderStatusView(generics.GenericAPIView):
    serializer_class = serializers.DeleteOrderStatusSerializer

    def delete(self, request, order_id, *args, **kwargs):
        order = get_object(models.Order, id=order_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.validated_data['comment']
        order.rejected_comment = comment
        order.status = OrderStatus.REJECTED
        order.save()

        log_com = (f"Buyurtma O'chirildi!!! \n"
                   f"Comment: {comment}\n")
        order.create_log(
            action=OrderLogActions.DELETE,
            user=request.user,
            comment=log_com,
        )
        SocketSendOrders.ws_dispatcher_orders(action='d', order=order)
        SocketSendOrders.ws_filling_orders(action='d', order=order)
        SocketSendOrders.ws_status_orders(action='d', order=order)

        return Response({'msg': "Success"}, status=status.HTTP_204_NO_CONTENT)
