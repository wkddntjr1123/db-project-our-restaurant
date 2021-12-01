from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout, name="logout"),
    path("check_id/", views.check_Id, name="checkId"),
    path("mypage/", views.mypage, name="account"),
    path("change_password/", views.changePassword, name="changePassword"),
    path("account_update/", views.accountUpdate, name="accountUpdate"),
    path("management/", views.user_management, name="management"),
    # group update
    path("create-group/", views.createGroup),
    path("invite-user/", views.inviteUser),
    path("accept-invite/", views.acceptInvite),
    path("decline-invite/", views.declineInvite),
    path("get-own-group-data/", views.getOwnGroupData),
    path("get-my-group-data/", views.getMyGroupData),
    path("get-invite-data/", views.getInvitedData),
]
