from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

from users.api.v4.serializers import UserLoginSerializer, UserSignupSerializer


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        response_data = {
            'user_id': user.id,
            'username': user.username,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        } if (serializer.is_valid() and
              (user := serializer.validated_data) and
              (refresh := RefreshToken.for_user(user))) else serializer.errors

        return Response(
            response_data,
            status=status.HTTP_200_OK if serializer.is_valid() else status.HTTP_400_BAD_REQUEST
        )


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)

        response_data = {
            'user_id': user.id,
            'username': user.username,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        } if (serializer.is_valid() and
              (user := serializer.save()) and
              (refresh := RefreshToken.for_user(user))) else serializer.errors

        return Response(
            response_data,
            status=status.HTTP_201_CREATED if serializer.is_valid() else status.HTTP_400_BAD_REQUEST
        )
