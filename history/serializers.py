from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from history.models import UserHistory
from searchapp.models import User, MarkedUrl


class UserHistorySerializer(serializers.ModelSerializer):
    """"""

    last_visit_time = serializers.ReadOnlyField(source=('get_last_visit_time_formate'))

    class Meta:
        model = UserHistory
        fields = "__all__"

