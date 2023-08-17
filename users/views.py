import jwt
import requests
from django.conf import settings
from django.contrib import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, exceptions
from . import serializers, models
from users.models import User


class Me(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise exceptions.ParseError("Enter password")
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):
    def get_object(self, username):
        try:
            return models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, username):
        user = self.get_object(username)
        serializer = serializers.TinyUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise exceptions.ParseError
        if user.check_password(old_password):
            if user.check_password(old_password) == user.check_password(new_password):
                raise exceptions.ParseError("Same as before passwored")
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError
        user = auth.authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            auth.login(request, user)
            return Response({"ok": "Done"})
        else:
            return Response({"error": "Wrong password"})


class LogOut(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        auth.logout(request)
        return Response({"bye": "bye"})


class JWTLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError
        user = auth.authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode({"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256")
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


class GithubLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = (
                requests.get(
                    f"http://github.com/login/oauth/access_token?code={code}&client_id=72af9d41820cb7329816&client_secret={settings.GITHUB_SECRET}",
                    headers={"Accept": "application/json"},
                )
                .json()
                .get("access_token")
            )
            user_data = requests.get(
                "http://api.github.com/user",
                headers={
                    "Accept": "application/json",
                    "Authorization": "Bearer " + access_token,
                },
            ).json()
            user_emails = requests.get(
                "http://api.github.com/user/emails",
                headers={
                    "Accept": "application/json",
                    "Authorization": "Bearer " + access_token,
                },
            ).json()
            try:
                user = User.objects.get(email=user_emails[0]["email"])
                auth.login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    username=user_data.get("login"),
                    name=user_data.get("name"),
                    avatar=user_data.get("avatar_url"),
                    email=user_emails[0]["email"],
                )
                user.set_unusable_password()
                user.save()
                auth.login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = (
                requests.post(
                    "https://kauth.kakao.com/oauth/token",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data={
                        "grant_type": "authorization_code",
                        "client_id": "d7fe98d70f4dac645708afc3086b987f",
                        "reidrect_url": "http://127.0.0.1:3000/social/kakao",
                        "code": code,
                    },
                )
                .json()
                .get("access_token")
            )
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Bearer {access_token}",
                },
            ).json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                auth.login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    name=profile.get("nickname"),
                    username=profile.get("nickname"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
                auth.login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
