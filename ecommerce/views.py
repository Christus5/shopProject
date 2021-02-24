from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.generic import View, DeleteView, ListView

from ecommerce.models import *


@method_decorator(login_required, name='dispatch')
class HomeView(View):
    template_name = 'ecommerce/home.html'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        user = request.user
        orders = user.order_set.all()

        return render(request, self.template_name, {
            'user': user,
            'orders': orders
        })


@method_decorator(login_required, name='dispatch')
class ItemView(View):
    template_name = 'ecommerce/item_details.html'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        try:
            item = Item.objects.get(pk=request.GET.get('item_id'))
        except:
            return redirect(to='ecommerce:home')

        return render(request, self.template_name, {
            'item': item
        })

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        try:
            item = Item.objects.get(pk=request.GET.get('item_id'))
            if item.quantity == 0 or not item.available:
                return redirect(to='ecommerce.home')
            Item.objects.filter(pk=item.pk).update(quantity=F('quantity') - 1)
        except:
            return redirect(to='ecommerce:home')

        user = request.user
        order = Order(item=item, user=user, cart=user.cart_set.last(), price=item.price)
        order.save()
        return redirect(to='ecommerce:order', order_id=order.id)


@method_decorator(login_required, name='dispatch')
class OrderDetailsView(View):
    template_name = 'ecommerce/order_details.html'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        order = get_object_or_404(Order, pk=kwargs['order_id'])
        return render(request, self.template_name, {
            'order': order
        })

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        return render(request, self.template_name, {
        })


@method_decorator(login_required, name='dispatch')
class CartDetailsView(View):
    template_name = 'ecommerce/cart_details.html'

    def get(self, request, *args, **kwargs) -> 'HttpResponse':
        cart = get_object_or_404(request.user.cart_set, pk=kwargs['cart_id'])

        if not cart.is_active:
            messages.error(request, 'Invalid access to cart')
            return redirect(to='ecommerce:home')

        return render(request, self.template_name, {
            'cart': cart
        })

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        user = request.user
        cart = get_object_or_404(request.user.cart_set, pk=kwargs['cart_id'])

        if user.balance >= cart.get_total_price():
            return redirect(to='ecommerce:home')

        messages.error(request, 'Insufficient funds!')
        return render(request, self.template_name, {
            'cart': cart
        })


@method_decorator(login_required, name='dispatch')
class StoreView(ListView):
    template_name = 'ecommerce/store.html'
    model = Item
    paginate_by = 4
    context_object_name = 'items'
