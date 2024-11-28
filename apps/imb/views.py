from asgiref.sync import async_to_sync
from django.conf import settings
from django.db.models import When, Case, IntegerField
from rest_framework import views, generics, viewsets
from rest_framework.response import Response
from telegram import InputMediaPhoto, Bot

from apps.checkout import models as checkout_models
from apps.users.external import EXTERNAL_USERS
from utils import IMBPermission, get_object, APIException
from utils.choices import TransactionTypes
from utils.customs import IMBAuthentication
from . import serializers, models
from apps.orders.models import Order


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

    def get_queryset(self):
        order = self.request.query_params.get('order', 'image_count')
        qs = models.Contact.objects.annotate(
            image_count=(
                    Case(
                        When(trailer_front__isnull=False, trailer_front__gt='', then=1),
                        default=0, output_field=IntegerField()
                    ) +
                    Case(
                        When(trailer_back__isnull=False, trailer_back__gt='', then=1),
                        default=0, output_field=IntegerField()
                    ) +
                    Case(
                        When(license_front__isnull=False, license_front__gt='', then=1),
                        default=0, output_field=IntegerField()
                    ) +
                    Case(
                        When(license_back__isnull=False, license_back__gt='', then=1),
                        default=0, output_field=IntegerField()
                    ) +
                    Case(
                        When(track_front__isnull=False, track_front__gt='', then=1),
                        default=0, output_field=IntegerField()
                    ) +
                    Case(
                        When(track_back__isnull=False, track_back__gt='', then=1),
                        default=0, output_field=IntegerField()
                    )
            )
        ).order_by(order)
        return qs


class SendToTelegramView(views.APIView):
    BOT_TOKEN = settings.DUMP_BOT_TOKEN
    CHAT_ID = settings.DRIVER_CONTACTS

    def get(self, request, phone: str, order_id: int, *args, **kwargs):

        if phone and phone.isdigit() and len(phone) != 12:
            raise APIException('Phone number must be 12 digits')

        phone = phone[3::]

        contact = get_object(model=models.Contact, phone=phone)
        order = get_object(model=Order, id=order_id, select_related=['loading', 'unloading'])

        self.send(contact, caption=self.get_caption(contact, order=order))

        return Response({'phone': phone, 'contact_id': contact.id})

    def send(self, contact, caption: str):
        bot = Bot(token=self.BOT_TOKEN)
        media_group = []
        fields = ('trailer_front', 'trailer_back', 'license_front', 'license_back', 'track_front', 'track_back')
        for field in fields:
            if item := getattr(contact, field):
                media_group.append(InputMediaPhoto(item))
        chat_id = self.request.user.chat_id
        if media_group:
            _last = media_group.pop()
            media_group.append(InputMediaPhoto(_last.media, caption=caption))
            async_to_sync(bot.send_media_group)(chat_id=chat_id, media=media_group)
        else:
            async_to_sync(bot.send_message)(chat_id=chat_id, text=caption)

    @staticmethod
    def get_caption(contact, order):
        return (
            f'Haydovchi: {contact.full_name}\n'
            f'Telefon raqami: {contact.phone}\n'
            f'Moshina Raqami: {contact.truck_id}\n'
            f'Moshina modeli: {contact.car_model}\n'
            f'Moshina turi: {contact.car_type}\n'
            f'Tirkama turi: {contact.trailer_type}\n'
            f'Buyurtma: {order.code}\n'
            f'Sana: {order.date}\n'
            f"Yo'nalish: {order.loading.name} -> {order.unloading.name}\n"
        )
