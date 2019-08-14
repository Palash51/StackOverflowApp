from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from Stackexchange.response import api_response
from helpers import get_logged_user
from history.models import UserHistory
from history.serializers import UserHistorySerializer
from searchapp.models import MarkedUrl


class UserHistoryAPIView(APIView):
    """user's local history"""

    @api_response
    def get(self, request):
        user = get_logged_user()
        user_history = UserHistory.objects.filter(user=user)
        data = UserHistorySerializer(user_history, many=True).data

        return {"status": 1, "data": data}


class DashboardAPIView(APIView):
    """user data on dashboard"""


    @api_response
    def get(self, request):
        user = get_logged_user()

        user_history = UserHistory.objects.filter(user=user)
        marked_url = MarkedUrl.objects.filter(user=user)

        data = {
            "total_marked_URL": marked_url.count(),
            "total_visited_URL": user_history.count()

        }

        # response = {'success': 'true', 'errors': "", 'data': user_data}

        return {"status": 1, "data": data}


