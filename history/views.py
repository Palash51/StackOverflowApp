from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from Stackexchange.response import api_response


class UserHistoryAPIView(APIView):
    """user's local history"""

    permission_classes = (IsAuthenticated,)


    @api_response
    def get(self, request):
        return