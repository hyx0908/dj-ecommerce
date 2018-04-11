from django.conf.urls import url

from .views import OrderListView, OrderDetailView


urlpatterns = [
    url(r'^$', OrderListView.as_view() , name='list'),
    url(r'^detail/(?P<order_id>[0-9a-zA-Z]+)/$', OrderDetailView.as_view(), name='order-detail')
]