from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from users.models import User


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get("username"), password=data.get("password"))

        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials")

        return user


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_fields):
        return User.objects.create_user(
            username=validated_fields['username'],
            password=validated_fields['password']
        )
