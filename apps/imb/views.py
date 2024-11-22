from rest_framework import views, generics, viewsets
from rest_framework.response import Response

from apps.checkout import models as checkout_models
from apps.users.external import EXTERNAL_USERS
from utils import IMBPermission, get_object, APIException
from utils.choices import TransactionTypes
from utils.customs import IMBAuthentication
from . import serializers, models


class CheckoutBalanceView(views.APIView):
    permission_classes = (IMBPermission,)
    authentication_classes = (IMBAuthentication,)

    def get(self, request):
        return Response({'current_balance': checkout_models.MainCheckout.balance})


class TransactionsView(generics.ListCreateAPIView):
    permission_classes = (IMBPermission,)
    authentication_classes = (IMBAuthentication,)
    serializer_class = serializers.IMBTransactionSerializer
    queryset = checkout_models.Transaction.objects.all().order_by('-id')
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
            model=checkout_models.Transaction,
            id=self.kwargs['pk'],
            type=TransactionTypes.EXPENSE,
        )

    def perform_update(self, serializer):
        serializer.save(receiver=EXTERNAL_USERS.imb_user)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.IMBContactSerializer
    queryset = models.Contact.objects.all().order_by('-updated_at')
    http_method_names = ('get', 'post', 'patch', 'delete')
    search_fields = ('full_name', 'phone', 'truck_id')


class SendToTelegramView(views.APIView):

    def get(self, request, phone, *args, **kwargs):

        if phone and len(phone) != 12:
            raise APIException('Phone number must be 12 digits')

        phone = phone[3::]

        contact = get_object(model=models.Contact, phone=phone)

        return Response({'phone': phone, 'contact_id': contact.id})

    @staticmethod
    def send(contact):
        pass
