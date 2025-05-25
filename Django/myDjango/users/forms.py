from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super(AuthUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password"].label = ""
        self.fields["username"].widget = forms.TextInput(
            attrs={
                "placeholder": "Имя пользователя",
                "class": "form-control",
            }
        )
        self.fields["password"].widget = forms.TextInput(
            attrs={
                "placeholder": "Пароль",
                "class": "form-control",

            }
        )


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password1"].label = ""
        self.fields["password2"].label = ""
        self.fields["username"].widget = forms.TextInput(
            attrs={
                "placeholder": "Имя пользователя",
                "class": "form-control",
            }
        )
        self.fields["password1"].widget = forms.TextInput(
            attrs={
                "placeholder": "Пароль",
                "class": "form-control",

            }
        )
        self.fields["password2"].widget = forms.TextInput(
            attrs={
                "placeholder": "Подтвердите пароль",
                "class": "form-control",

            }
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["username"].help_text = ""
        self.fields["username"].widget = forms.TextInput(
            attrs={
                 "placeholder": "Имя пользователя",
                 "class": "form-control",
            }
        )
        self.fields["first_name"].label = ""
        self.fields["first_name"].help_text = ""
        self.fields["first_name"].widget = forms.TextInput(
            attrs={
                "placeholder": "Имя ",
                "class": "form-control",
             }
        )
        self.fields["last_name"].label = ""
        self.fields["last_name"].help_text = ""
        self.fields["last_name"].widget = forms.TextInput(
            attrs={
                "placeholder": "Фамилия",
                "class": "form-control",
             }
        )
        self.fields["email"].label = ""
        self.fields["email"].help_text = ""
        self.fields["email"].widget = forms.TextInput(
            attrs={
                "placeholder": "Электронная почта",
                "class": "form-control",
            }
        )