from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from products.models import Product
from orders.models import Order

from .forms import ContactForm


def home_page(request):
    products = Product.objects.all().count()
    orders = Order.objects.all().count()

    context = {
        'title': 'Welcome!',
        'products': products,
        'orders': orders,
    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    if contact_form.is_valid():
        if request.is_ajax():
            json_data = {
                "message": "Thank you for message!"
            }
            return JsonResponse(json_data)

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type="application/json")

    context = {
        "title": "Contact",
        "contact_form": contact_form,
    }
    return render(request, 'contact/view.html', context)
