from django.conf import settings
from asgiref.sync import async_to_sync
from django.db.models import Count, When, Case, IntegerField, ExpressionWrapper, Q, F
from rest_framework import views, generics, viewsets
from rest_framework.response import Response
from telegram import InputMediaPhoto, Bot

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
    http_method_names = ('get', 'post', 'patch', 'delete')
    search_fields = ('full_name', 'phone', 'truck_id')
    query = """
        SELECT *,
               (CASE WHEN trailer_front IS NOT NULL AND trailer_front != '' THEN 1 ELSE 0 END +
                CASE WHEN trailer_back IS NOT NULL AND trailer_back != '' THEN 1 ELSE 0 END +
                CASE WHEN license_front IS NOT NULL AND license_front != '' THEN 1 ELSE 0 END +
                CASE WHEN license_back IS NOT NULL AND license_back != '' THEN 1 ELSE 0 END +
                CASE WHEN track_front IS NOT NULL AND track_front != '' THEN 1 ELSE 0 END +
                CASE WHEN track_back IS NOT NULL AND track_back != '' THEN 1 ELSE 0 END
               ) AS image_count
        FROM contacts
        ORDER BY image_count DESC
    """

    def get_queryset(self):
        qs = models.Contact.objects.using('imb').raw(self.query)
        return qs


class SendToTelegramView(views.APIView):
    BOT_TOKEN = settings.DUMP_BOT_TOKEN
    CHAT_ID = settings.DRIVER_CONTACTS

    def get(self, request, phone: str, *args, **kwargs):

        if phone and phone.isdigit() and len(phone) != 12:
            raise APIException('Phone number must be 12 digits')

        phone = phone[3::]

        contact = get_object(model=models.Contact, phone=phone)

        self.send(contact)

        return Response({'phone': phone, 'contact_id': contact.id})

    def send(self, contact):
        bot = Bot(token=self.BOT_TOKEN)
        media_group = []
        fields = ('trailer_front', 'trailer_back', 'license_front', 'license_back', 'track_front', 'track_back')
        caption = self.get_caption(contact)
        for field in fields:
            if item := getattr(contact, field):
                media_group.append(InputMediaPhoto(item))

        _last = media_group.pop()
        media_group.append(InputMediaPhoto(_last.media, caption=caption))

        async_to_sync(bot.send_media_group)(chat_id=self.CHAT_ID, media=media_group)

    @staticmethod
    def get_caption(contact):
        return (
            f'Haydovchi: {contact.full_name}\n'
            f'Moshina Raqami: {contact.truck_id}\n'
            f'Moshina modeli: {contact.car_model}\n'
            f'Moshina turi: {contact.car_type}\n'
            f'Tirkama turi: {contact.trailer_type}\n'
        )
