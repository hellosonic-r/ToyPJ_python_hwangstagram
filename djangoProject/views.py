# views.py를 통해 url을 호출했을 때 내가 만든 main.html 을 표시할 수 있게 만들어줄 수 있다
from django.shortcuts import render
from rest_framework.views import APIView


class Sub(APIView):
    def get(self, request):
        print("겟으로 호출")
        return render(request, "hwangstagram/main.html")

    def post(self, request):
        print("포스트로 호출")
        return render(request, "hwangstagram/main.html")