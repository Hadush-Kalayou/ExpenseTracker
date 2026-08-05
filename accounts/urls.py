from django.urls import path
#from django.views.generic import RedirectView
from . import views

urlpatterns = [

    # Home
 # Home
path(
    "",
    views.home_view,
    name="home"
),

    # Authentication
    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Profile
    path(
        "profile/",
        views.profile_view,
        name="profile"
    ),

    path(
        "profile/edit/",
        views.edit_profile_view,
        name="profile_edit"
    ),

    # Password
    path(
        "change-password/",
        views.change_password_view,
        name="change_password"
    ),

    path(
        "forgot-password/",
        views.ForgotPasswordView.as_view(),
        name="forgot_password"
    ),

    path(
        "reset-password/<uidb64>/<token>/",
        views.ResetPasswordView.as_view(),
        name="password_reset_confirm"
    ),
]