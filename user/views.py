from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from uuid import uuid4
import os
from djangoProject.settings import MEDIA_ROOT


class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        # TODO 회원가입
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        if User.objects.filter(email=email).exists():
            return Response(status=500, data=dict(message="이미 존재하는 이메일 계정입니다."))
        elif User.objects.filter(nickname=nickname).exists():
            return Response(status=500, data=dict(message="이미 존재하는 닉네임입니다."))

        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_image="default_profile.jpg")

        return Response(status=200, data=dict(message="회원가입에 성공했습니다. 로그인 해주세요."))


class Login(APIView):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # TODO 로그인
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email is None:
            return Response(status=500, data=dict(message="이메일을 입력해주세요."))

        if password is None:
            return Response(status=500, data=dict(message="비밀번호를 입력해주세요."))

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=500, data=dict(message="이메일 혹은 비밀번호를 잘못 입력했습니다."))

        if check_password(password, user.password) is False:
            return Response(status=500, data=dict(message="이메일 혹은 비밀번호를 잘못 입력했습니다."))

        request.session['email'] = email

        return Response(status=200, data=dict(message="로그인에 성공했습니다."))


class Logout(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")


class UploadProfile(APIView):
    def post(self, request):

        # 일단 파일 불러와
        file = request.FILES['file']
        email = request.data.get('email')

        uuid_name = uuid4().hex
        save_path = os.path.join(MEDIA_ROOT, uuid_name)

        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image = uuid_name

        user = User.objects.filter(email=email).first()

        user.profile_image = profile_image
        user.save()

        return Response(status=200)
