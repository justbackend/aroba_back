from rest_framework.response import Response
from rest_framework import views, generics


class ClientListView(views.APIView):

    def get(self, request):
        return Response({})
