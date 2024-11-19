from rest_framework import views, generics
from rest_framework.response import Response

from .. import models
from . import serializers

from utils import IMBPermission
from utils.customs import IMBAuthentication
from utils.choices import TransactionTypes
from apps.users.external import EXTERNAL_USERS


class CheckoutView(views.APIView):
    permission_classes = (IMBPermission,)
    authentication_classes = (IMBAuthentication,)

    def get(self, request):
        return Response({'current_balance': models.MainCheckout.balance})


class TransactionsView(generics.ListCreateAPIView):
    permission_classes = (IMBPermission,)
    authentication_classes = (IMBAuthentication,)
    serializer_class = serializers.IMBTransactionSerializer
    queryset = models.Transaction.objects.all().order_by('-id')

    def perform_create(self, serializer):
        serializer.save(
            type=TransactionTypes.INCOME,
            creator=EXTERNAL_USERS.imb_user
        )
