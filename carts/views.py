from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from addresses.forms import AddressForm
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order
from products.models import Product
from .models import Cart


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        "title": product.title,
        "price": product.price,
        "url": product.get_absolute_url(),
        "id": product.id
    } for product in cart_obj.products.all()]
    cart_data = {
        "products": products,
        "total": cart_obj.total,
        "subtotal": cart_obj.subtotal,
    }
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {
        'cart': cart_obj,
    }
    return render(request, 'carts/home.html', context)


def cart_update(request):
    product_id = request.POST.get('product_id')
    product_obj = None
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            redirect('carts:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            product_added = False
        else:
            cart_obj.products.add(product_obj)  # product_id
            product_added = True

        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            json_data = {
                "added": product_added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data)
        return redirect('cart:home')


def checkout_home(request):
    cart_obj, new_cart = Cart.objects.new_or_get(request)
    if new_cart or cart_obj.products.count() == 0:
        return redirect('cart:home')
    order_obj = None
    address_qs = None
    billing_address_qs = None
    shipping_address_qs = None
    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressForm()
    shipping_address_id = request.session.get('shipping_address_id', None)
    billing_address_id = request.session.get('billing_address_id', None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        if request.user.is_authenticated():
            address_qs = Address.objects.filter(billing_profile=billing_profile)
            shipping_address_qs = address_qs.filter(address_type='shipping')
            billing_address_qs = address_qs.filter(address_type='billing')
        order_obj, created_obj = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order_obj.save()

    if request.method == 'POST':
        is_done = order_obj.check_order_done()
        if is_done:
            order_obj.mark_paid()
            del request.session['cart_id']
            request.session['cart_items'] = 0
            return redirect('cart:checkout_done')

    context = {
        'order_obj': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'shipping_address_qs': shipping_address_qs,
        'billing_address_qs': billing_address_qs,

    }
    return render(request, 'carts/checkout.html', context)


def checkout_done_view(request):
    return render(request, 'carts/checkout_done.html')
