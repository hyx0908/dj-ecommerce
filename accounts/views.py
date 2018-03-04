from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, FormView, DetailView, View
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail, EmailVerification
from .signals import user_logged_in

User = settings.AUTH_USER_MODEL


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/account_home.html'

    def get_object(self, queryset=None):
        return self.request.user


class AccountEmailActivationView(View):
    def get(self, request, key, *args, **kwargs):
        qs = EmailVerification.objects.filter(key__iexact=key)
        confirmable_qs = qs.confirmable()
        if confirmable_qs.count() == 1:
            obj = confirmable_qs.first()
            obj.activate()
            messages.success(request, 'Your email has been confirmed. You can login.')
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
        return render(request, 'registration/activation-error.html', {})


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
    return redirect(reverse('register'))


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.user
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if user:
            if not user.is_active:
                messages.error(request, "This user is inactive")
                return super(LoginView, self).form_valid(form)  # form_invalid ?

            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)

            if 'quest_email_id' in request.session:
                del request.session['guest_email_id']

            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")

        return super(LoginView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context


# def login_page(request):
#     form = LoginForm(request.POST or None)
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#
#     context = {
#         "login_form": form,
#     }
#     return render(request, 'accounts/login.html', context)

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['register_form'] = RegisterForm()
        return context

    # def form_valid(self, form):
    #     # request = self.request
    #     user = form.save(commit=False)
    #     user.save()
    #     # login(request, user)

# def register_page(request):
#     form = RegisterForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect("/")
#     context = {
#         "register_form": form,
#     }
#     return render(request, 'accounts/register.html', context)
