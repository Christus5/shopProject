from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.utils.decorators import method_decorator

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, DeleteView

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
class ItemView(DetailView):
    model = Item
    template_name = 'ecommerce/item_details.html'
    context_object_name = 'item'

    def post(self, request, *args, **kwargs) -> 'HttpResponse':
        try:
            item = self.get_object()
            if item.quantity == 0 or not item.available:
                return redirect(to='ecommerce.home')
            Item.objects.filter(pk=item.pk).update(quantity=F('quantity') - 1)
        except:
            return redirect(to='ecommerce:home')

        user = request.user
        order = Order(item=item, user=user, cart=user.cart_set.last(), price=item.price)
        order.save()
        return redirect(to='ecommerce:order', pk=order.pk)


@method_decorator(login_required, name='dispatch')
class OrderView(DetailView):
    model = Order
    template_name = 'ecommerce/order/order_details.html'
    context_object_name = 'order'

    def get_queryset(self):
        return self.request.user.order_set


@method_decorator(login_required, name='dispatch')
class OrderDeleteView(DeleteView):
    model = Order
    success_url = '/ecommerce/'
    template_name = 'ecommerce/order/order_confirm_delete.html'


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
