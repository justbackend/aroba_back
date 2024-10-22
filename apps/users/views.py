from rest_framework import views, generics, viewsets, response


class SalomView(views.APIView):

    def get(self, request):
        return response.Response({})
