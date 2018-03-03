from django.conf.urls import url

from .views import (
    ProductListView,
    ProductDetailView,
    # ProductFeaturedListView,
    # ProductFeaturedDetailView
)

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='product-list'),
    # url(r'^(?P<prod_pk>\d+)/$', ProductDetailView.as_view()),
    url(r'^(?P<prod_slug>[\w-]+)/$', ProductDetailView.as_view(), name='product-detail'),
]
