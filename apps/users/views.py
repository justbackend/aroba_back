from rest_framework import views, response


class SalomView(views.APIView):

    def get(self, request, *args, **kwargs):
        return response.Response({})
