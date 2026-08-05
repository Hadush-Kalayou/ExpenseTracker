from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash



from .forms import (
    RegisterForm,
    LoginForm,
    ProfileUpdateForm,
    CustomPasswordChangeForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)

from django.contrib.auth import get_user_model

User = get_user_model()


# =====================================================
# Register View
# =====================================================
def register_view(request):

    if request.user.is_authenticated:
        return redirect("profile")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                "Registration completed successfully."
            )

            return redirect("login")

    else:

        form = RegisterForm()

    context = {
        "form": form
    }

    return render(
        request,
        "accounts/register.html",
        context
    )

#home view
def home_view(request):
    return render(request, "home.html")
# =====================================================
# Login View
# =====================================================
def login_view(request):

    # If the user is already logged in
    if request.user.is_authenticated:

        if request.user.is_staff:
            return redirect("admin_dashboard")

        return redirect("user_dashboard")

    # Login form
    form = LoginForm(request, data=request.POST or None)

    # Login submitted
    if request.method == "POST":

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    f"Welcome {user.full_name}"
                )

                if user.is_staff:
                    return redirect("admin_dashboard")

                return redirect("user_dashboard")

            else:

                messages.error(
                    request,
                    "Invalid username/email or password."
                )

    # IMPORTANT: This must always be at the end
    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


# =====================================================
# Logout View
# =====================================================
@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have logged out successfully."
    )

    return redirect("login")


from django.contrib.auth import update_session_auth_hash


# =====================================================
# Profile View
# =====================================================
@login_required
def profile_view(request):

    return render(
        request,
        "accounts/profile.html",
        {
            "user": request.user
        }
    )



# =====================================================
# Edit Profile View
# =====================================================
@login_required
def edit_profile_view(request):

    if request.method == "POST":

        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        "accounts/profile_edit.html",
        {
            "form": form
        }
    )


# =====================================================
# Change Password
# =====================================================
@login_required
def change_password_view(request):

    if request.method == "POST":

        form = CustomPasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect("profile")

    else:

        form = CustomPasswordChangeForm(
            request.user
        )

    return render(
        request,
        "accounts/change_password.html",
        {
            "form": form
        }
    )


# =====================================================
# Forgot Password
# =====================================================
class ForgotPasswordView(PasswordResetView):

    template_name = "accounts/forgot_password.html"

    email_template_name = "accounts/password_reset_email.html"

    subject_template_name = "accounts/password_reset_subject.txt"

    success_url = reverse_lazy("login")

    form_class = CustomPasswordResetForm


# =====================================================
# Reset Password
# =====================================================
class ResetPasswordView(PasswordResetConfirmView):

    template_name = "accounts/reset_password.html"

    success_url = reverse_lazy("login")

    form_class = CustomSetPasswordForm