from rest_framework import views, generics, viewsets, response
from rest_framework_simplejwt.authentication import JWTAuthentication


class SalomView(views.APIView):

    def get(self, request):
        return response.Response({})
