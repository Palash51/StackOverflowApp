from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from searchapp.models import User, MarkedUrl


class SignupSerializer(serializers.ModelSerializer):
    """
    signup serializer will validate user input
    unique email and mobile no and return specific message
    """
    class Meta:
        model = User
        fields = ('email', 'mobile_number')

    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Email already exists")
        ])
    mobile_number = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all(), message="Mobile already exists")
        ])


    @property
    def sg_errors(self):
        messages = ""
        for error in self.errors:
            messages += self.errors[error][0]
            messages += "\n"

        return messages


class StackOverflowQuestionSerializer(serializers.Serializer):
    """get the json data for each query"""
    json = serializers.ReadOnlyField()



class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "mobile_number")


class MarkedUrlSerializer(serializers.ModelSerializer):
    """serialize markedurl model"""

    user = UserSerializer(read_only=True)
    created_at = serializers.ReadOnlyField(source=('get_created_at_time_formate'))
    # url = serializers.HyperlinkedIdentityField(view_name='marked', read_only=True)

    class Meta:
        model = MarkedUrl
        fields = "__all__"