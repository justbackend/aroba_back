from django.db.models import Prefetch, F, Sum, Exists, OuterRef
from rest_framework import generics, views
from rest_framework.response import Response

import utils
from apps.clients import models as client_models
from apps.orders import models as order_models
from utils.choices import *
from utils.excel import *
from apps.checkout import models, serializers
from apps.checkout.models import MainCheckout


class ReportOrdersListAPI(generics.ListAPIView):
    serializer_class = serializers.ReportSerializer

    def get_queryset(self):
        if not (payment_type := self.request.query_params.get('payment_type')):
            raise utils.APIException('Must provide payment type. Example: ?payment_type=cash')

        orders_qs = (
            order_models.Order.objects.filter(
                payment_type=payment_type,
                status__gte=OrderStatus.STARTED,
            )
            .annotate(
                loading_name=F('loading__name'),
                unloading_name=F('unloading__name'),
                invoice_status=F('invoice__status'),
            )
            .exclude(paid=True, client_paid=True)
        )

        return (
            client_models.Client.objects
            .prefetch_related(Prefetch('orders', queryset=orders_qs, to_attr='to_orders'))
            .annotate(
                has_orders=Exists(orders_qs.filter(client=OuterRef('pk'))),
            )
            .filter(orders__isnull=False, has_orders=True)
            .distinct()
        )


class PayOrder(views.APIView):

    def get(self, request, order_id: int, *args, **kwargs):
        order = utils.get_object(order_models.Order, paid=False, id=order_id)
        order.paid = True
        order.status = OrderStatus.FINISHED
        order.save()
        log_comment = (f"Furaga chiqim qilindi\n\n"
                       f"{order.car_number}\n"
                       f"{order.driver_phone}\n"
                       f"Summa: {order.total_amount}")
        order.create_log(comment=log_comment, action=OrderLogActions.PAID, user=request.user)

        MainCheckout - order.total_amount # noqa

        return Response(data={'order_id': order_id, 'client_id': order.client_id})


class RollbackPaidOrder(generics.GenericAPIView):
    serializer_class = serializers.RollbackOrderCommentSerializer

    def post(self, request, order_id: int, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.validated_data['comment']

        order = utils.get_object(order_models.Order, paid=True, id=order_id)
        order.paid = False
        order.status = OrderStatus.STARTED
        order.save()
        log_comment = (f"To'lov qilngan reys qaytarildi\n\n"
                       f"{order.car_number}\n"
                       f"{order.driver_phone}\n"
                       f"Summa: {order.total_amount}\n"
                       f"Komentariya: {comment}")
        order.create_log(comment=log_comment, action=OrderLogActions.ROLLBACK_PAID, user=request.user)

        MainCheckout + order.total_amount # noqa

        return Response(data={'order_id': order_id, 'client_id': order.client_id})


class PayClientOrder(views.APIView):
    def get(self, request, order_id: int, *args, **kwargs):
        order = utils.get_object(order_models.Order, client_paid=False, id=order_id, select_related=['client'])
        order.client_paid = True
        order.save()

        MainCheckout + order.income # noqa

        log_comment = (f"Klient tomonidan kirim [Naqt]\n\n"
                       f"Klient: {order.client.name}\n"
                       f"{order.car_number}\n"
                       f"{order.driver_phone}\n"
                       f"Summa: {order.income}")

        order.create_log(comment=log_comment, action=OrderLogActions.CLIENT_PAID, user=request.user)

        return Response(data={'order_id': order_id, 'client_id': order.client_id})


class RollbackClientPaidOrder(generics.GenericAPIView):
    serializer_class = serializers.RollbackOrderCommentSerializer

    def post(self, request, order_id: int, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.validated_data['comment']

        order = utils.get_object(order_models.Order, client_paid=True, id=order_id, select_related=['client'])
        order.client_paid = False
        order.save()
        MainCheckout - order.income  # noqa

        log_comment = (f"Kirim bo'lgan buyurtma puli qaytarildi\n\n"
                       f"Klient: {order.client.name}\n"
                       f"{order.car_number}\n"
                       f"{order.driver_phone}\n"
                       f"Summa: {order.income}\n"
                       f"Komnetariya: {comment}")

        order.create_log(comment=log_comment, action=OrderLogActions.ROLLBACK_CLIENT_PAID, user=request.user)
        return Response(data={'order_id': order_id, 'client_id': order.client_id})


class CreateTransactionAPI(generics.ListCreateAPIView):
    queryset = models.Transaction.objects.all().order_by('-id')
    filterset_fields = ('type', 'status')

    serializer_classes = {
        'POST': serializers.CreateTransactionSerializer,
        'GET': serializers.TransactionListSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes[self.request.method]

    def perform_create(self, serializer):
        serializer.save(type=TransactionTypes.EXPENSE)


class TransactionsExcel(ExcelListView):
    data = models.Transaction.objects.all().order_by('-id')
    filename = 'transactions'
    fields = ['id', 'amount', 'status', 'type', 'comment', 'created_at']
    filters = ['type', ]


class UpdateTransactionAPI(generics.UpdateAPIView):
    serializer_class = serializers.TransactionStatusUpdateSerializer
    http_method_names = 'put',

    def get_object(self):
        return utils.get_object(model=models.Transaction, id=self.kwargs['pk'], type=TransactionTypes.INCOME)

    def perform_update(self, serializer):
        serializer.save(receiver=self.request.user)


class BalanceView(views.APIView):
    def get(self, request):
        current_balance = MainCheckout.balance

        response = {'current_balance': current_balance}

        unpaid_orders = (
            order_models.Order.objects.filter(
                client_paid=False,
                status__gte=OrderStatus.STARTED
            )
            .values('payment_type')
            .annotate(total=Sum('income', default=0))
        )

        for item in unpaid_orders:
            response[item['payment_type']] = item['total']

        return Response(response)


class SummaryListView(generics.ListAPIView):
    serializer_class = serializers.CashSummarySerializer
    filterset_fields = ('client', 'loading', 'unloading', 'payment_type')
    search_fields = ('code', 'car_number', 'driver_phone',)

    def get_queryset(self):
        return (
            order_models.Order.objects.filter(
                status__gte=OrderStatus.STARTED
            )
            .select_related('loading', 'unloading', 'client')
            .only(
                'id', 'code', 'date', 'car_number', 'loading__name', 'payment_type',
                'unloading__name', 'client__name', 'total_amount', 'paid', 'income', 'client_paid'
            ).order_by('-id')
        )


class SummaryExcelView(ExcelListView):
    fields = ('id', 'code', 'date', 'car_number', 'loading_name', 'unloading_name', 'client_name')
    filename = 'cash_summary'

    def get_data(self):
        return (
            order_models.Order.objects.filter(
                payment_type=OrderPaymentTypes.CASH,
                paid=True,
            )
            .values(
                'id', 'code', 'date', 'car_number',
                loading_name=F('loading__name'), unloading_name=F('unloading__name'), client_name=F('client__name'),
            ))


class SummaryOrderUpdateAPI(generics.UpdateAPIView):
    serializer_class = serializers.SummaryOrderUpdateSerializer
    http_method_names = 'put',

    def get_object(self):
        return utils.get_object(
            model=order_models.Order,
            id=self.kwargs['order_id'],
        )
