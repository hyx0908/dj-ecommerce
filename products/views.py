from django.views.generic import ListView, DetailView
from django.http import Http404

from analytics.mixins import ObjectViewedMixin
from carts.models import Cart

from .models import Product


class ProductFeaturedListView(ListView):
    template_name = 'products/product_list.html'
    queryset = Product.objects.features()


class ProductFeaturedDetailView(ObjectViewedMixin, DetailView):
    template_name = 'products/featured_detail.html'
    queryset = Product.objects.all().featured()


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.all().order_by('timestamp')


class ProductDetailView(ObjectViewedMixin, DetailView):
    model = Product
    slug_url_kwarg = 'prod_slug'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get('prod_slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found.")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Wrong way!")
        return instance
