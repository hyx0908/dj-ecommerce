from django.utils.http import is_safe_url
from django.urls import reverse


class RequestFormMixin(object):
    def get_form_kwargs(self):
        kwargs = super(RequestFormMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class NextURLMixin(object):
    default_next = '/'

    def get_next_url(self):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        if is_safe_url(redirect_path, request.get_host()):
            return redirect_path
        return reverse('home')
