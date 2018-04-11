from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

from carts.views import cart_detail_api_view
from .views import home_page, contact_page


urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^contact/$', contact_page, name='contact'),
    url(r'^api/cart/', cart_detail_api_view, name='api-cart'),
    url(r'^accounts/$', RedirectView.as_view(url='/account')),
    url(r'^account/', include('accounts.urls', namespace='accounts')),
    url(r'^accounts/', include('accounts.passwords.urls')),
    url(r'^cart/', include('carts.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^search/', include('search.urls', namespace='search')),

    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
