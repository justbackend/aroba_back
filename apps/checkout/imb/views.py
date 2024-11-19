from rest_framework.response import Response
from rest_framework import views, generics, viewsets

from utils import IMBPermission
from utils.customs import IMBAuthentication


class CheckoutView(views.APIView):
    pass


class TransactionsView(generics.ListCreateAPIView):
    pass
