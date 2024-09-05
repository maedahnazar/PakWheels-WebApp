from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, fields):
        user = authenticate(username=fields.get("username"), password=fields.get("password"))

        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials")

        return user


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_fields):
        return User.objects.create_user(
            username=validated_fields['username'],
            password=validated_fields['password']
        )
