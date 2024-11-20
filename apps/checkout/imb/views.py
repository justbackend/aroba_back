from rest_framework import views, generics
from rest_framework.response import Response

from .. import models
from . import serializers

from utils import IMBPermission, get_object
from utils.customs import IMBAuthentication
from utils.choices import TransactionTypes
from apps.users.external import EXTERNAL_USERS


class CheckoutBalanceView(views.APIView):
    permission_classes = (IMBPermission,)
    authentication_classes = (IMBAuthentication,)

    def get(self, request):
        return Response({'current_balance': models.MainCheckout.balance})


class TransactionsView(generics.ListCreateAPIView):
    permission_classes = (IMBPermission,)
    authentication_classes = (IMBAuthentication,)
    serializer_class = serializers.IMBTransactionSerializer
    queryset = models.Transaction.objects.all().order_by('-id')
    filterset_fields = ('type',)

    def perform_create(self, serializer):
        serializer.save(
            type=TransactionTypes.INCOME,
            creator=EXTERNAL_USERS.imb_user
        )


class UpdateTransactionView(generics.UpdateAPIView):
    permission_classes = (IMBPermission,)
    authentication_classes = (IMBAuthentication,)
    serializer_class = serializers.IMBUpdateTransactionSerializer
    http_method_names = 'put',

    def get_object(self):
        return get_object(
            model=models.Transaction,
            id=self.kwargs['pk'],
            type=TransactionTypes.EXPENSE,
        )

    def perform_update(self, serializer):
        serializer.save(receiver=EXTERNAL_USERS.imb_user)
