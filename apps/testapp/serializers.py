from rest_framework import serializers
from apps.testapp.models import User


class GoogleAuthSerializer(serializers.Serializer):
    code = serializers.CharField(
        required=True,
        help_text="Одноразовый code, полученный от Google",
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "role")
        read_only_fields = ("id", "email", "role")