from rest_framework import views, generics
from .. import models
from . import serializers

from utils import IMBPermission
from utils.customs import IMBAuthentication


class CheckoutView(views.APIView):
    permission_classes = (IMBPermission,)
    authentication_classes = (IMBAuthentication,)
    pass


class TransactionsView(generics.ListCreateAPIView):
    permission_classes = (IMBPermission,)
    authentication_classes = (IMBAuthentication,)
    serializer_class = serializers.IMBTransactionSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            pass
        return
