from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import GuestEmail, EmailVerification
from .signals import user_logged_in

User = get_user_model()


class EmailReactivationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):  # _email
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if not qs.exists():
            register_link = reverse("accounts:register")
            msg = """This email does not exist. Do you want to <a href="{link}">register</a>?
            """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))

        qs_email = EmailVerification.objects.email_exists(email)
        if not qs_email.exists():
            msg = "This email has been activated."
            raise forms.ValidationError(mark_safe(msg))
        return email


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

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')

        qs = User.objects.filter(email=email)
        if qs.exists():
            not_active = qs.filter(is_active=False)
            # print("not active")
            print(not_active)
            if not_active.exists():
                resend_activation_link = reverse('accounts:email_resend_activation')

                is_confirmable = EmailVerification.objects.filter(email=email).confirmable()
                if is_confirmable.exists():
                    msg = """Check your email in order to confirm your account or go to 
                    <a href="{link}">resend activation link</a>""".format(link=resend_activation_link)
                    raise forms.ValidationError(mark_safe(msg))

                not_verified = EmailVerification.objects.email_exists(email)
                print("not verified")
                print(not_verified)
                if not_verified.exists():
                    print("not_verified inside")

                    msg = """You should verify your email first. Do you want to <a href="{link}">resend activation link</a>?
                    """.format(link=resend_activation_link)
                    raise forms.ValidationError(mark_safe(msg))

                if not not_verified or not is_confirmable:
                    raise forms.ValidationError("This user is inactive.")

        user = authenticate(request, username=email, password=password)
        if not user:
            raise forms.ValidationError("Wrong email or password")
        login(request, user)
        self.user = user
        user_logged_in.send(user.__class__, instance=user, request=request)
        if 'quest_email_id' in request.session:
            del request.session['guest_email_id']

        return data


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean(self):  # _password2
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
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
