from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from products.views import UserProductHistoryView
from .views import (
    GuestRegisterView,
    RegisterView,
    LoginView,
    AccountHomeView,
    AccountEmailActivationView,
    UserDetailUpdateView,
)

urlpatterns = [
    url(r'^$', AccountHomeView.as_view(), name='home'),

    url(r'^detail/update/$', UserDetailUpdateView.as_view(), name='detail_update'),
    url(r'^history/products/$', UserProductHistoryView.as_view(), name='history_products'),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/guest/$', GuestRegisterView.as_view(), name='guest_register'),

    url(r'^email/confirm/(?P<key>[0-9A-Za-z]+)/$', AccountEmailActivationView.as_view(), name='email_activate'),
    url(r'^email/resend-activation/$', AccountEmailActivationView.as_view(), name='email_resend_activation'),
]
