from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import GuestEmail, EmailVerification

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]


class GuestForm(forms.ModelForm):
    class Meta:
        model = GuestEmail
        fields = ['email']


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        self.user = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        self.user = authenticate(username=email, password=password)

        if not self.user:
            raise forms.ValidationError('Wrong email or password')

        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user

# class RegisterForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(
#         widget=forms.PasswordInput
#     )
#     password2 = forms.CharField(
#         label="Confirm password",
#         widget=forms.PasswordInput
#     )
#     email = forms.EmailField()
#
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         qs = User.objects.filter(username=username)
#         if qs.exists():
#             raise forms.ValidationError("Username is taken")
#         return username
#
#     def clean_email(self):
#         email = self.cleaned_data['email']
#         qs = User.objects.filter(email=email)
#         if qs.exists():
#             raise forms.ValidationError("Email is taken")
#         return email
#
#     def clean(self):
#         data = self.cleaned_data
#         password = self.cleaned_data.get('password')
#         password2 = self.cleaned_data.get('password2')
#
#         if password2 != password:
#             raise forms.ValidationError("Password must match!")
#         return data
