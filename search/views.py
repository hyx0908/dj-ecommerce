from django.views.generic import ListView

from products.models import Product


class SearchProductListView(ListView):
    template_name = 'search/search_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductListView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q')
        if query:
            if query is not None:
                return Product.objects.search(query)
        return Product.objects.none()
