from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe

from ecommerce.mixins import NextURLMixin, RequestFormMixin
from .forms import LoginForm, RegisterForm, GuestForm, EmailReactivationForm, UserDetailUpdateForm
from .models import GuestEmail, EmailVerification

User = settings.AUTH_USER_MODEL


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/account_home.html'

    def get_object(self, queryset=None):
        return self.request.user


class AccountEmailActivationView(NextURLMixin, FormMixin, View):
    form_class = EmailReactivationForm
    success_url = reverse_lazy('accounts:login')

    key = None

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailVerification.objects.filter(key__iexact=key)
            confirmable_qs = qs.confirmable()
            if confirmable_qs.count() == 1:
                obj = confirmable_qs.first()
                obj.activate()
                messages.success(request, 'Your email has been successfully confirmed. You can login.')
                return redirect('accounts:login')
            else:
                activated_qs = qs.filter(activated=True)
                if activated_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = """Your email has been confirmed.
                    Do you need to <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.success(request, mark_safe(msg))
                    return redirect('accounts:login')

        context = {
            'form': self.get_form(),
            'key': key
        }
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)  ## tutaj jest False, SPRAWDZIĆ TUTAJ !!!

    def form_valid(self, form):
        msg = "Activation link sent, please check your email."
        request = self.request
        messages.success(request, msg)
        email = form.cleaned_data.get('email')
        obj = EmailVerification.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailVerification.objects.create(user=user, email=email)
        new_activation.send_email_verification()
        qs = EmailVerification.objects.exclude(key__exact=new_activation.key).filter(user=user, email=email)
        if qs.exists():
            qs.delete()
        next_path = self.get_next_url()
        return redirect(next_path)

    def form_invalid(self, form):
        context = {
            'form': self.get_form(),
            "key": self.key
        }
        return render(self.request, 'registration/activation-error.html', context)


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email, new_guest_email_created = GuestEmail.objects.get_or_create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
    return redirect(reverse('accounts:register'))


class GuestRegisterView(NextURLMixin, RequestFormMixin, CreateView):
    form_class = GuestForm
    default_next = reverse_lazy('accounts:register')

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)


class LoginView(NextURLMixin, RequestFormMixin, FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    # success_url = reverse_lazy('home')

    default_next = reverse_lazy('home')

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        request = self.request
        context['login_form'] = LoginForm(request=request)
        return context


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')


class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailUpdateForm
    template_name = 'accounts/user_detail_update.html'
    success_url = reverse_lazy('accounts:home')

    def get_object(self, queryset=None):
        return self.request.user