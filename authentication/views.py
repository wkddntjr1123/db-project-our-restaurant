from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from .models import Group, User
from django.http.response import JsonResponse


@csrf_exempt
def signup(request):
    if request.method == "POST":  # POST
        new_user = User()
        new_user.user_id = request.POST["username"]
        new_user.set_password(request.POST["password"])  # 비밀번호 암호화해서 저장
        new_user.name = request.POST["name"]
        new_user.nickname = request.POST["email"]
        new_user.is_active = True
        new_user.save()  # DB에 저장하고
        auth.login(request, new_user)  # 로그인후 메인페이지로
        return redirect("restaurant:index")
    else:  # GET으로 오면 회원가입 양식 띄워주기
        return render(request, "user/signup.html")


@csrf_exempt
def login(request):
    if request.method == "POST":  # POST
        username = request.POST["username"]
        password = request.POST["password"]

        try:  # 유저가 있으면 user에 저장되고
            user = User.objects.get(user_id=username)
        except:  # 유저가 없으면 excetion에러를 None으로 처리
            user = None

        if user is not None:  # 해당 아이디가 있을경우
            if not user.is_active:  # 비활성화 상태면(이메일인증X)
                return render(request, "user/login.html")
            else:  # 계정이 있는데 활성화 상태면(이메일인증o)
                user = auth.authenticate(
                    request, user_id=username, password=password
                )  # 해당 비밀번호가 맞는지 확인
                if user is not None:  # 아이디 비밀번호 일치하는 계정이 존재하면
                    auth.login(request, user)  # 로그인
                    request.session["user"] = user.id
                    return redirect("restaurant:index")
                else:  # 비밀번호가 틀리다면
                    context = {"error": "잘못된 비밀번호입니다."}
                    return render(request, "user/login.html", context)
        else:  # 계정이 없으면
            context = {"error": "등록되지 않는 ID입니다."}
            return render(request, "user/login.html", context)

    else:  # GET
        return render(request, "user/login.html")


def logout(request):
    auth.logout(request)
    return redirect("restaurant:index")


@csrf_exempt
def check_Id(request):
    try:
        user = User.objects.get(user_id=request.GET["username"])
    except Exception as e:
        user = None

    result = {
        "data": "not exist" if (user == None) else "exist",
    }
    return JsonResponse(result)


def mypage(request):
    user = request.user  # 계정정보를 누른 유저
    return render(request, "user/account.html", {"user": user})


@csrf_exempt
def changePassword(request):
    if request.method == "POST":
        user_id = request.user.id
        username = User.objects.get(pk=user_id).user_id
        password = request.POST["password_before"]
        user = auth.authenticate(request, user_id=username, password=password)
        if user is None:
            context = {"not_same_error": True}
            return render(request, "user/change_password.html", context)
        if request.POST["new_password"] != request.POST["new_password_confirm"]:
            context = {"new_not_same_error": True}
            return render(request, "user/change_password.html", context)
        user.set_password(request.POST["new_password"])
        user.save()
        auth.logout(request)
        return redirect("restaurant:index")
    else:
        return render(request, "user/change_password.html")


@csrf_exempt
def accountUpdate(request):
    user = request.user
    if request.method == "POST":
        user.name = request.POST["name_"]
        user.nickname = request.POST["email_"]
        user.save()
        return redirect("authentication:account")
    return render(request, "user/account_update.html", {"user": user})


@csrf_exempt
def user_management(request):
    groups = Group.objects.all()
    return render(request, "user/management.html", {"groups": groups})
