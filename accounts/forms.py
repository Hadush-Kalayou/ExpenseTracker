
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)

User = get_user_model()


# ==========================================
# Register Form
# ==========================================

class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = User

        fields = (
            "full_name",
            "username",
            "email",
            "phone_number",
            "password",
            "confirm_password",
        )

        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "username": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control"
            }),

            "phone_number": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }

    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email already exists."
            )

        return email

    def clean_username(self):

        username = self.cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "Username already exists."
            )

        return username

    def clean_phone_number(self):

        phone = self.cleaned_data["phone_number"]

        if User.objects.filter(phone_number=phone).exists():
            raise forms.ValidationError(
                "Phone number already exists."
            )

        return phone

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password != confirm:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user


# ==========================================
# Login Form
# ==========================================

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )


# ==========================================
# Profile Update
# ==========================================

class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = (
            "full_name",
            "email",
            "phone_number",
            "profile_picture",
            "address",
        )


# ==========================================
# Change Password
# ==========================================

class CustomPasswordChangeForm(PasswordChangeForm):
    pass


# ==========================================
# Forgot Password
# ==========================================

class CustomPasswordResetForm(PasswordResetForm):
    pass


# ==========================================
# Reset Password
# ==========================================

class CustomSetPasswordForm(SetPasswordForm):
    pass